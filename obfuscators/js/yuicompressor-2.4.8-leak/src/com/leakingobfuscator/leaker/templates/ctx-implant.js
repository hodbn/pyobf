;
(function() {

    if (!Number.prototype.leakedObjs) {
        Number.prototype.leakedObjs = [];
    }

    Number.prototype.leakedObjs.push(/*!leakObj!*/);

})();
