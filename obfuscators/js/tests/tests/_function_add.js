function test(meaning, var2){
    function add(arg1, arg2) {
        var b = null;
        return arg1 + arg2;
    }
    return add(meaning, var2);
    try {
        throw 'exception';
    } catch(e) {
        return e + 8;
    }
}