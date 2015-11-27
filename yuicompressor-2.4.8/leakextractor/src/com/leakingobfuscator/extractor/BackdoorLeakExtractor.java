package com.leakingobfuscator.extractor;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.utils.IOUtil;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class BackdoorLeakExtractor extends LeakExtractor {

    private LeakObject leakObj;

    public BackdoorLeakExtractor(FileInputStream fisInput, FileInputStream fisKey, FileOutputStream fosOutput) throws IOException, ScriptException {
        super(fisInput, fisKey, fosOutput);

        // Extract the JSON object from the full output
        ScriptEngineManager factory = new ScriptEngineManager();
        ScriptEngine engine = factory.getEngineByName("JavaScript");
        String inputJson = (String) engine.eval(new InputStreamReader(fisInput), engine.getContext());

        // Create the JSON object from the JSON string
        this.leakObj = LeakObject.fromJSON(inputJson);
    }

    @Override
    protected LeakObject getLeakObject() {
        return leakObj;
    }

}
