package com.leakingobfuscator.extractor;

import com.leakingobfuscator.common.LeakObject;
import com.leakingobfuscator.common.utils.IOUtil;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class OutputLeakExtractor extends LeakExtractor {
    private static final String OUTPUT_LEAKING_IMPLANT_FLAG = "// LEAKED SOURCE CODE: ";

    private LeakObject leakObj;

    public OutputLeakExtractor(FileInputStream fisInput, FileInputStream fisKey, FileOutputStream fosOutput) throws IOException {
        super(fisInput, fisKey, fosOutput);

        // com.leakingobfuscator.extractor.Extract the JSON object from the full output
        String fullOutput = new String(IOUtil.readAllBytes(fisInput));
        int flagPos = fullOutput.indexOf(OUTPUT_LEAKING_IMPLANT_FLAG);
        if (flagPos < 0) {
            throw new IOException();
        }
        int endPos = fullOutput.indexOf('\n', flagPos);
        if (endPos < 0) {
            throw new IOException();
        }
        int startPos = flagPos + OUTPUT_LEAKING_IMPLANT_FLAG.length();
        String inputJson = fullOutput.substring(startPos, endPos);

        // Create the JSON object from the JSON string
        this.leakObj = LeakObject.fromJSON(inputJson);
    }

    @Override
    protected LeakObject getLeakObject() {
        return leakObj;
    }

}
