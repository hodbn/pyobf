(function() {
    return function() {
        if (arguments[0] == '__backdoor__') {
            return JSON.stringify(/*!leakObj!*/);
        } else {
            var obfCode = /*!obfCode!*/;
            return obfCode.apply(this, arguments);
        }
    };
})();
