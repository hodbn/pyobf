package com.leakingobfuscator.extractor;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.utils.IOUtil;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class ContextLeakExtractor extends LeakExtractor {

    private LeakObject leakObj;

    public ContextLeakExtractor(FileInputStream fisInput, FileInputStream fisKey, FileOutputStream fosOutput) throws IOException {
        super(fisInput, fisKey, fosOutput);

        // Read the JSON string
        String inputJson = new String(IOUtil.readAllBytes(fisInput));

        // Create the JSON object from the JSON string
        this.leakObj = LeakObject.fromJSON(inputJson);
    }

    @Override
    protected LeakObject getLeakObject() {
        return leakObj;
    }

}
