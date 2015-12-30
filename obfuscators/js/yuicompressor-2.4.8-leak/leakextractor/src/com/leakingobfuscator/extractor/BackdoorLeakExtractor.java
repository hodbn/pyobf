package com.leakingobfuscator.extractor;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.utils.IOUtil;
import jdk.nashorn.api.scripting.ScriptObjectMirror;
import jdk.nashorn.internal.runtime.ScriptFunction;

import javax.script.ScriptContext;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class BackdoorLeakExtractor extends LeakExtractor {

    private static final String BACKDOOR_MAGIC = "__backdoor__";

    private LeakObject leakObj;

    public BackdoorLeakExtractor(FileInputStream fisInput, FileInputStream fisKey, FileOutputStream fosOutput) throws IOException, ScriptException {
        super(fisInput, fisKey, fosOutput);

        // Setup a JavaScript engine
        ScriptEngineManager factory = new ScriptEngineManager();
        ScriptEngine engine = factory.getEngineByName("JavaScript");

        // Get the wrapper function
        ScriptObjectMirror wrapperFunc = (ScriptObjectMirror) engine.eval(new InputStreamReader(fisInput));

        // Call the wrapper function with the backdoor magic
        engine.put("func", wrapperFunc);
        String inputJson = (String) engine.eval("func('" + BACKDOOR_MAGIC + "');");

        // Create the JSON object from the JSON string
        this.leakObj = LeakObject.fromJSON(inputJson);
    }

    @Override
    protected LeakObject getLeakObject() {
        return leakObj;
    }

}
