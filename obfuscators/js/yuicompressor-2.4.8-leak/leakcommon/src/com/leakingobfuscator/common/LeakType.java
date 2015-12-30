package com.leakingobfuscator.common;

public enum LeakType {

    LEAK_TYPE_OUTPUT("output"),
    LEAK_TYPE_CONTEXT("context"),
    LEAK_TYPE_BACKDOOR("backdoor"),
    ;

    private final String text;

    public static LeakType fromText(String text) {
        if (text != null) {
            for (LeakType t : LeakType.values()) {
                if (text.equalsIgnoreCase(t.text)) {
                    return t;
                }
            }
        }
        return null;
    }

    private LeakType(final String text) {
        this.text = text;
    }

    @Override
    public String toString() {
        return text;
    }

}
