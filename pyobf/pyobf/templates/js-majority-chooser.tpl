function {{prog_name}}() {
    var
        progs = [{% for prog in progs  %}
            {{prog.code|unsafeescapejs}},{% endfor %}
        ],
        out = [],
        freq = {},
        max = 0,
        result
    ;
    for (var i = 0; i < progs.length; i++) {
        var p = progs[i];
        eval(p);
        out.push({{prog_name}}.apply(this, arguments));
    }
    for (var i = 0; i < out.length; i++) {
        var v = out[i];
        freq[v] = (freq[v] || 0) + 1;
        if (freq[v] > max) {
            max = freq[v];
            result = v;
        }
    }
    return result;
}
