package com.leakingobfuscator.leaker.implant;

import com.leakingobfuscator.common.utils.IOUtil;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public class ImplantTemplate {

    private static final char FROM_SPLITTER = ':';
    private static final char OPT_WRAP_STRING = 's';
    private static final char OPT_IN_CODE = 'c';

    public static String generate(String templateFn, HashMap<String, String> replacements) throws IOException {
        // Read the template as a resource
        InputStream is = ImplantTemplate.class.getResourceAsStream(templateFn);
        String tpl = new String(IOUtil.readAllBytes(is));

        for (Map.Entry<String, String> replacement : replacements.entrySet()) {
            String from = replacement.getKey(),
                    to = replacement.getValue();
            int pos;
            String opts = null;

            // Process options if available
            if ((pos = from.indexOf(FROM_SPLITTER)) > -1) {
                opts = from.substring(0, pos);
                from = "!" + from.substring(pos + 1) + "!";
            } else {
                from = "!" + from + "!";
            }

            // Process options if available
            if (opts != null) {
                boolean isWrapString = (opts.indexOf(OPT_WRAP_STRING) > -1);
                boolean inCode = (opts.indexOf(OPT_IN_CODE) > -1);

                if (isWrapString) {
                    to = "\"" + to + "\"";
                }
                if (inCode) {
                    from = "/*" + from + "*/";
                }
            }

            tpl = tpl.replace(from, to);
        }

        return tpl;
    }

}
