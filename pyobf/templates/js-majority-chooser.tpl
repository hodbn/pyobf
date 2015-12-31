(function() {
    var
        out = [
        {% for prog in progs  %}
            ({{prog}}).apply(this, arguments),
        {% endfor %}
        ],
        freq = {},
        max = 0,
        result
    ;
    for (var v in out) {
        freq[out[v]] = (freq[out[v]] || 0) + 1;
        if (freq[out[v]] > max) {
            max = out[out[v]];
            result = out[v];
        }
    }
    return result;
})();
