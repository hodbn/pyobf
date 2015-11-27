function test(a, b){
    function add(arg1, arg2) {
        var b = null;
        return arg1 + arg2;
    }
    return add(a, b);
    try {
        throw 'exception';
    } catch(e) {
        return e + 8;
    }
}