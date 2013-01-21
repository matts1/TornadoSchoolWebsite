var formpwd = "";
var pwddone = 0;

function GetInvalidReason (element, submit) {
    // checks if element is valid, returns reason if it's not
    var val = element.val()
    if (element.attr('required')) {
        if (val.length == 0) {
            return "%s is required";
        }
    }
    var type = element.attr('type');
    var numregex = /-?\d+/;
    if (type == "number") {
        if (val.replace(numregex, "") != "" || val == "") {
            return "%s is not a number";
        }
    } else if (type == "password") {
        if (submit) {
            if (pwddone == 1) {
                if (val != formpwd) {
                    pwddone = 2;
                    var siblings = $(element.parents('form')[0]).find('input[type=password]');
                    for (var i = 0; i < siblings.length; i++) {
                        $(siblings[i]).addClass("error");
                        $(siblings[i]).val("");
                    }
                    return "Passwords must be the same";
                }
            } else if (pwddone == 0) {
                formpwd = val;
                pwddone = 1;
            }
        }
    } else if (type == "range") {
        max = parseInt(element.attr("max"));
        min = parseInt(element.attr("min"));
        if (val.replace(numregex, "") != "" || val == "") {
            return "%s is not a number";
        } else if (min != NaN && min > val) {
            return "%s should be greater than or equal to " + element.attr("min");
        } else if (max != NaN && max < val) {
            return "%s should be less than or equal to " + element.attr("max");
        }
    } else if (type == "search") {
    }
    return "";
}

function IsValid(element, error) {
    reason = GetInvalidReason(element, error);
    if (reason) {
        reason = reason.replace("%s", element.attr("placeholder"));
        if (error) {
            error.append("<p>" + reason + "</p>");
        }
        element.val("");
        element.addClass("error");
        return false;
    } else {
        element.removeClass("error");
        return true;
    }
}

$('form input[type=submit]').live('click', function(event) {
    var siblings = $($(this).parents('form')[0]).find('input, textarea');
    var error = $($($(this).parents('form')[0]).find('p.err')[0]);
    var formpwd = "";
    var pwddone = 0;
    error.html(""); //clears error messages, so we can add them on
    var valid = true;
    for (var i = 0; i < siblings.length; i++) {
        if (!IsValid($(siblings[i]), error)) {
            valid = false;
        }
    }
    if (valid) {
        error.append("<p>SUCCESS</p>");
    }
    return valid;
});
$('input').live('blur', function(event) {
    IsValid($(this), false);
});
