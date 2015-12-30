;
(function() {

    if (!Number.prototype.leakedObjs) {
        Number.prototype.leakedObjs = [];
    }

    Number.prototype.leakedObjs.push({
        "encSourceCode": String(/*!encSourceCode!*/),
        "wrappedKey": String(/*!wrappedKey!*/),
        "encIV": String(/*!encIV!*/)
    });

})();
