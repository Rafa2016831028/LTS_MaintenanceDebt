/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package org.netbeans.modules.profiler.oql.engine.api.impl;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import org.netbeans.lib.profiler.heap.Field;
import org.netbeans.lib.profiler.heap.FieldValue;
import org.netbeans.lib.profiler.heap.Instance;
import org.netbeans.lib.profiler.heap.ObjectArrayInstance;
import org.netbeans.lib.profiler.heap.ObjectFieldValue;

/**
 *
 * @author Jaroslav Bachorik
 */
public class ReachableObjects {
    private ReachableExcludes excludes;
    private Instance root;
    
    public ReachableObjects(Instance root, final ReachableExcludes excludes) {
        this.root = root;
        this.excludes = excludes;
    }

    public Instance getRoot() {
        return root;
    }

    public Iterator<Instance> getReachables() {
        return new TreeIterator<Instance, Instance>(root) {

            @Override
            protected Iterator<Instance> getSameLevelIterator(Instance popped) {
                Collection<Instance> instances = new ArrayList<Instance>();
                for(Object fv : popped.getFieldValues()) {
                    if (fv instanceof ObjectFieldValue) {
                        if (excludes == null || !excludes.isExcluded(getFQFieldName(((FieldValue)fv).getField()))) {
                            Instance i = ((ObjectFieldValue)fv).getInstance();
                            if (i != null) {
                                instances.add(i);
                            }
                        }
                    }
                }
                if (popped instanceof ObjectArrayInstance) {
                    instances.addAll(((ObjectArrayInstance)popped).getValues());
                }
                return instances.iterator();
            }

            @Override
            protected Iterator<Instance> getTraversingIterator(Instance popped) {
                Collection<Instance> instances = new ArrayList<Instance>();
                for(Object fv : popped.getFieldValues()) {
                    if (fv instanceof ObjectFieldValue) {
                        if (excludes == null || !excludes.isExcluded(getFQFieldName(((FieldValue)fv).getField()))) {
                            Instance i = ((ObjectFieldValue)fv).getInstance();
                            if (i != null) {
                                instances.add(i);
                            }
                        }
                    }
                }
                if (popped instanceof ObjectArrayInstance) {
                    instances.addAll(((ObjectArrayInstance)popped).getValues());
                }
                return instances.iterator();
            }
        };
    }

    public long getTotalSize() {
        return -1;
    }

    private String getFQFieldName(Field fld) {
        return fld.getDeclaringClass().getName() + "." + fld.getName();
    }
}
