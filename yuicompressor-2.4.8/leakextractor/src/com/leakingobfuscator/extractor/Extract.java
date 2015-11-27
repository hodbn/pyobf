package com.leakingobfuscator.extractor;

import com.leakingobfuscator.common.LeakType;
import jargs.gnu.CmdLineParser;

import javax.script.ScriptException;
import java.io.*;

public class Extract {

    public static void main(String[] args) {
        CmdLineParser parser = new CmdLineParser();
        CmdLineParser.Option typeOpt = parser.addStringOption("leaktype");
        CmdLineParser.Option helpOpt = parser.addBooleanOption('h', "help");
        CmdLineParser.Option outFnOpt = parser.addStringOption('o', "output");
        CmdLineParser.Option keyFnOpt = parser.addStringOption('k', "leakkey");

        try {
            parser.parse(args);
            String[] inFns = parser.getRemainingArgs();

            Boolean isHelp = (Boolean) parser.getOptionValue(helpOpt);
            if (isHelp != null && isHelp) {
                usage();
                System.exit(0);
            }

            String outFn = (String) parser.getOptionValue(outFnOpt);
            String keyFn = (String) parser.getOptionValue(keyFnOpt);

            if (inFns.length == 0 || inFns.length > 1) {
                usage();
                System.exit(1);
            }
            String inFn = inFns[0];

            LeakType leakType = LeakType.fromText((String) parser.getOptionValue(typeOpt));

            if (leakType == null) {
                usage();
                System.exit(1);
            }

            if (extract(inFn, keyFn, outFn, leakType)) {
                System.exit(0);
            } else {
                System.exit(1);
            }

        } catch (CmdLineParser.OptionException e) {
            usage();
            System.exit(1);
        }
    }

    private static boolean extract(String inFn, String keyFn, String outFn, LeakType leakType) {
        FileInputStream fisInput = null;
        try {
            fisInput = new FileInputStream(inFn);
        } catch (FileNotFoundException e) {
            System.err.println("Input file not found");
            System.exit(1);
        }
        FileInputStream fisKey = null;
        try {
            fisKey = new FileInputStream(keyFn);
        } catch (FileNotFoundException e) {
            System.err.println("Key file not found");
            System.exit(1);
        }
        FileOutputStream fosOutput = null;
        try {
            fosOutput = new FileOutputStream(outFn);
        } catch (IOException e) {
            System.err.println("Output file not found");
            System.exit(1);
        }
        try {
            if (leakType == null) {
                return false;
            } else {
                switch (leakType) {
                    case LEAK_TYPE_CONTEXT:
                        new ContextLeakExtractor(fisInput, fisKey, fosOutput).extract();
                        break;
                    case LEAK_TYPE_OUTPUT:
                        new OutputLeakExtractor(fisInput, fisKey, fosOutput).extract();
                        break;
                    case LEAK_TYPE_BACKDOOR:
                        new BackdoorLeakExtractor(fisInput, fisKey, fosOutput).extract();
                        break;
                    default:
                        return false;
                }
            }
            return true;
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ScriptException e) {
            e.printStackTrace();
        } finally {
            try { fisInput.close(); } catch (IOException e) { e.printStackTrace(); }
            try { fisKey.close(); } catch (IOException e) { e.printStackTrace(); }
            try { fosOutput.close(); } catch (IOException e) { e.printStackTrace(); }
        }
        return false;
    }

    private static void usage() {
        System.err.println(
                "Leak extractor Version: @VERSION@\n"

                        + "\nUsage: java -jar leakextractor-@VERSION@.jar [options] -k [key file] -o [output file] [input file]\n"
                        + "\n"
                        + "Global Options\n"
                        + "  -h, --help                             Displays this information\n"
                        + "  --leaktype <context|output|backdoor>   Specifies the leak type\n"
                        + "  -k <keyfile>                           Take the key from <keyfile>.\n"
                        + "  -o <file>                              Place the output into <file>.\n");
    }

}
