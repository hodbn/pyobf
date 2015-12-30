package com.leakingobfuscator.leaker.templates;

import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class ScriptTemplate {

    private static final char OPT_SPLITTER = ':';
    private static final char OPT_WRAP_STRING = 's';
    private static final char OPT_IN_CODE = 'c';

    private static String replaceLine(String line, HashMap<String, String> replacements) {
        for (Map.Entry<String, String> replacement : replacements.entrySet()) {
            String from = replacement.getKey(),
                    to = replacement.getValue();
            int pos;
            String opts = null;

            // Process options if available
            if ((pos = from.indexOf(OPT_SPLITTER)) > -1) {
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

            line = line.replace(from, to);
        }

        return line;
    }

    public static void generate(String templateFn, Writer out, HashMap<String, String> replacements) throws IOException {
        // Read the template as a resource
        InputStream is = ScriptTemplate.class.getResourceAsStream(templateFn);
        replace(new InputStreamReader(is), out, replacements);
    }

    private static void replace(Reader in, Writer out, HashMap<String, String> replacements) throws IOException {
        BufferedReader reader = null;
        PrintWriter writer = null;

        try {
            reader = new BufferedReader(in);
            writer = new PrintWriter(out);
            String line;

            while ((line = reader.readLine()) != null) {
                writer.println(replaceLine(line, replacements));
            }
        } finally {
            if (reader != null) reader.close();
            if (writer != null) writer.close();
        }
    }

}
