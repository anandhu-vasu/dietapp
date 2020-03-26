function onSubmit() {
    if (validate('gender') & validate('age') & validate('height') & validate('weight') & validate('diet_plan') & validate('veg') & validate('occupation') & validate('disease') & validate('allergy')) {

        /*var data = {
            gender:$("[name='gender']:checked").val(),
            age:$("[name='age']").val(),
            height:$("[name='height']").val(),
            weight:$("[name='weight']").val(),
            diet_plan:$("[name='diet_plan']").val(),
            veg:$("[name='veg']").val(),
            occupation:$("[name='occupation']").val(),
            disease:$("[name='disease']").val(),
            allergy:$("[name='allergy']").val()
        }

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        var postdata = {
            data: JSON.stringify(data), csrfmiddlewaretoken: CSRFtoken
        };
        $.post('/form/', postdata,function(data){document.write(data)});*/
        return true
    }
    else return false
}
function validate(ele) {
    return $("[name='"+ele+"']").val() != "" ?
    $("[name='"+ele+"']").parent().removeClass("empty").addClass("valid") | true :
    $("[name='"+ele+"']").parent().removeClass("valid").addClass("empty") | false;
}
$(document).ready(function () {
    $('input[type=text]').on("input", (e) => {
        e.target.value = e.target.value.replace(/[^0-9.]/g,"");
        validate(e.target.name);
    })
});
