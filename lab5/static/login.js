function setPasswordHash(event) {
    const password = event.target.value;
    const passwordSHA256 = new jsSHA("SHA-256", "TEXT", { encoding: "UTF8" });
    passwordSHA256.update(password);
    jQuery("#id_password_hash").val(passwordSHA256.getHash("HEX"));
}