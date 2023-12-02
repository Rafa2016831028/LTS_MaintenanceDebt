//
//  ========================================================================
//  Copyright (c) 1995-2022 Mort Bay Consulting Pty Ltd and others.
//  ------------------------------------------------------------------------
//  All rights reserved. This program and the accompanying materials
//  are made available under the terms of the Eclipse Public License v1.0
//  and Apache License v2.0 which accompanies this distribution.
//
//      The Eclipse Public License is available at
//      http://www.eclipse.org/legal/epl-v10.html
//
//      The Apache License v2.0 is available at
//      http://www.opensource.org/licenses/apache2.0.php
//
//  You may elect to redistribute this code under either of these licenses.
//  ========================================================================
//

package org.eclipse.jetty.servlet;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;
import java.util.zip.GZIPInputStream;
import javax.servlet.MultipartConfigElement;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;

import org.eclipse.jetty.client.HttpClient;
import org.eclipse.jetty.client.api.ContentResponse;
import org.eclipse.jetty.client.api.Response;
import org.eclipse.jetty.client.util.BytesContentProvider;
import org.eclipse.jetty.client.util.InputStreamResponseListener;
import org.eclipse.jetty.client.util.MultiPartContentProvider;
import org.eclipse.jetty.client.util.StringContentProvider;
import org.eclipse.jetty.http.HttpFields;
import org.eclipse.jetty.http.HttpHeader;
import org.eclipse.jetty.http.HttpMethod;
import org.eclipse.jetty.http.HttpScheme;
import org.eclipse.jetty.http.MimeTypes;
import org.eclipse.jetty.http.MultiPartFormInputStream;
import org.eclipse.jetty.server.HttpChannel;
import org.eclipse.jetty.server.HttpConnectionFactory;
import org.eclipse.jetty.server.MultiPartFormDataCompliance;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.ServerConnector;
import org.eclipse.jetty.server.handler.gzip.GzipHandler;
import org.eclipse.jetty.util.IO;
import org.eclipse.jetty.util.log.Log;
import org.eclipse.jetty.util.log.Logger;
import org.eclipse.jetty.util.log.StacklessLogging;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.startsWith;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

public class MultiPartServletTest
{
    private static final Logger LOG = Log.getLogger(MultiPartServletTest.class);

    private Server server;
    private ServerConnector connector;
    private HttpClient client;
    private Path tmpDir;

    private static final int MAX_FILE_SIZE = 512 * 1024;
    private static final int LARGE_MESSAGE_SIZE = 1024 * 1024;

    public static Stream<Arguments> data()
    {
        return Arrays.asList(MultiPartFormDataCompliance.values()).stream().map(Arguments::of);
    }

    public static class MultiPartServlet extends HttpServlet
    {
        @Override
        protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
        {
            if (!req.getContentType().contains(MimeTypes.Type.MULTIPART_FORM_DATA.asString()))
            {
                resp.setContentType("text/plain");
                resp.getWriter().println("not content type " + MimeTypes.Type.MULTIPART_FORM_DATA);
                resp.getWriter().println("contentType: " + req.getContentType());
                return;
            }

            resp.setContentType("text/plain");
            for (Part part : req.getParts())
            {
                resp.getWriter().println("Part: name=" + part.getName() + ", size=" + part.getSize());
            }
        }
    }

    public static class MultiPartEchoServlet extends HttpServlet
    {
        @Override
        protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
        {
            if (!req.getContentType().contains(MimeTypes.Type.MULTIPART_FORM_DATA.asString()))
            {
                resp.sendError(400);
                return;
            }

            resp.setContentType(req.getContentType());
            IO.copy(req.getInputStream(), resp.getOutputStream());
        }
    }

    @BeforeEach
    public void start() throws Exception
    {
        tmpDir = Files.createTempDirectory(MultiPartServletTest.class.getSimpleName());
        assertNotNull(tmpDir);

        server = new Server();
        connector = new ServerConnector(server);
        server.addConnector(connector);

        MultipartConfigElement config = new MultipartConfigElement(tmpDir.toAbsolutePath().toString(),
            MAX_FILE_SIZE, -1, 1);

        ServletContextHandler contextHandler = new ServletContextHandler(ServletContextHandler.SESSIONS);
        contextHandler.setContextPath("/");
        ServletHolder servletHolder = contextHandler.addServlet(MultiPartServlet.class, "/");
        servletHolder.getRegistration().setMultipartConfig(config);
        servletHolder = contextHandler.addServlet(MultiPartEchoServlet.class, "/echo");
        servletHolder.getRegistration().setMultipartConfig(config);

        GzipHandler gzipHandler = new GzipHandler();
        gzipHandler.addIncludedMethods(HttpMethod.POST.asString());
        gzipHandler.addIncludedMimeTypes("multipart/form-data");
        gzipHandler.setMinGzipSize(32);
        gzipHandler.setHandler(contextHandler);
        server.setHandler(gzipHandler);

        server.start();

        client = new HttpClient();
        client.start();
        client.getContentDecoderFactories().clear();
    }

    @AfterEach
    public void stop() throws Exception
    {
        client.stop();
        server.stop();

        IO.delete(tmpDir.toFile());
    }

    @ParameterizedTest
    @MethodSource("data")
    public void testTempFilesDeletedOnError(MultiPartFormDataCompliance compliance) throws Exception
    {
        connector.getConnectionFactory(HttpConnectionFactory.class).getHttpConfiguration()
            .setMultiPartFormDataCompliance(compliance);

        byte[] byteArray = new byte[LARGE_MESSAGE_SIZE];
        for (int i = 0; i < byteArray.length; i++)
        {
            byteArray[i] = 1;
        }
        BytesContentProvider contentProvider = new BytesContentProvider(byteArray);

        MultiPartContentProvider multiPart = new MultiPartContentProvider();
        multiPart.addFieldPart("largePart", contentProvider, null);
        multiPart.close();

        try (StacklessLogging stacklessLogging = new StacklessLogging(HttpChannel.class, MultiPartFormInputStream.class))
        {
            ContentResponse response = client.newRequest("localhost", connector.getLocalPort())
                .scheme(HttpScheme.HTTP.asString())
                .method(HttpMethod.POST)
                .content(multiPart)
                .send();

            assertEquals(500, response.getStatus());
            assertThat(response.getContentAsString(),
                containsString("Multipart Mime part largePart exceeds max filesize"));
        }

        String[] fileList = tmpDir.toFile().list();
        assertNotNull(fileList);
        assertThat(fileList.length, is(0));
    }

    @Test
    public void testMultiPartGzip() throws Exception
    {
        String contentString = "the quick brown fox jumps over the lazy dog, " +
            "the quick brown fox jumps over the lazy dog";
        StringContentProvider content = new StringContentProvider(contentString);

        MultiPartContentProvider multiPart = new MultiPartContentProvider();
        multiPart.addFieldPart("largePart", content, null);
        multiPart.close();

        try (StacklessLogging ignored = new StacklessLogging(HttpChannel.class, MultiPartFormInputStream.class))
        {
            InputStreamResponseListener responseStream = new InputStreamResponseListener();
            client.newRequest("localhost", connector.getLocalPort())
                .path("/echo")
                .scheme(HttpScheme.HTTP.asString())
                .method(HttpMethod.POST)
                .header(HttpHeader.ACCEPT_ENCODING, "gzip")
                .content(multiPart)
                .send(responseStream);

            Response response = responseStream.get(5, TimeUnit.SECONDS);
            HttpFields headers = response.getHeaders();
            assertThat(headers.get(HttpHeader.CONTENT_TYPE), startsWith("multipart/form-data"));
            assertThat(headers.get(HttpHeader.CONTENT_ENCODING), is("gzip"));

            InputStream inputStream = new GZIPInputStream(responseStream.getInputStream());
            String contentType = headers.get(HttpHeader.CONTENT_TYPE);
            MultiPartFormInputStream mpis = new MultiPartFormInputStream(inputStream, contentType, null, null);
            List<Part> parts = new ArrayList<>(mpis.getParts());
            assertThat(parts.size(), is(1));
            assertThat(IO.toString(parts.get(0).getInputStream()), is(contentString));
        }
    }
}
