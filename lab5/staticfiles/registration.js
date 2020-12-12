function setPasswordHash(event) {
    const password = event.target.value;
    const passwordSHA256 = new jsSHA256("SHA-256", "TEXT", { encoding: "UTF8" });
    passwordSHA256.update(password);
    jQuery("#id_password").val(passwordSHA256.getHash("HEX"));
}

function setPasswordStrength(event) {
    const password = event.target.value;
    const passwordSHA1 = new jsSHA1("SHA-1", "TEXT", { encoding: "UTF8" });
    passwordSHA1.update(password.toLowerCase());
    const passwordSHA1hash = passwordSHA1.getHash("HEX");

    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            const regexp = /(?<token>[A-Z0-9]{35}):(?<quantity>\d+)/g;
            const tokenSuffix = passwordSHA1hash.slice(5).toUpperCase();
            let passwordMatches = 0;
            const matches = [...xhr.responseText.matchAll(regexp)];
            matches.forEach(match => {
                if (match.groups.token === tokenSuffix) {
                    passwordMatches += parseInt(match.groups.quantity);
                }
            });
            const passwordStrength = passwordMatches >= 1000
                ? 0
                : passwordMatches >= 100
                    ? 1
                    : passwordMatches >= 10
                        ? 2
                        : 3;
            console.log(passwordStrength);
            switch (passwordStrength) {
                case 0: jQuery("#password-strength-meter").val(0); jQuery("#password-strength-text").html("<img src='https://memepedia.ru/wp-content/uploads/2017/05/%D0%BD%D0%B5-%D0%B5%D1%88-%D0%BF%D0%BE%D0%B4%D1%83%D0%BC%D0%BE%D0%B9.jpg'>"); break;
                case 1: jQuery("#password-strength-meter").val(1); jQuery("#password-strength-text").html("<img src='https://www.meme-arsenal.com/memes/13f738becd18e66cbec27f94412c44df.jpg'>"); break;
                case 2: jQuery("#password-strength-meter").val(2); jQuery("#password-strength-text").html("<img src='https://i2.wp.com/bazara0.com/wp-content/uploads/2016/11/sesuriti_bazara0.jpg?fit=704%2C400&resize=1280%2C720'>"); break;
                case 3: jQuery("#password-strength-meter").val(3); jQuery("#password-strength-text").html("<img src='https://ic.pics.livejournal.com/sergeeffff/34028062/116402/116402_800.jpg'>"); break;
            }
        }
    }
    xhr.open('GET', `https://api.pwnedpasswords.com/range/${passwordSHA1hash.slice(0, 5)}`, true);
    xhr.send(null);
}