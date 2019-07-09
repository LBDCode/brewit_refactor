$("#submit-button").on("click", function(event) {
    event.preventDefault();

    var ingreds = [];
      $("table > tbody > tr").each(function() {
        var ing = {
            quantity: $(this).find('.quant').text(),
            unit: $(this).find('.unit').text(),
            description: $(this).find('.descrip').text()
        };
        ingreds.push(ing);
      });

      var recipe = {
        style_id: $("#style").val().trim(),
        name: $("#name").val().trim(),
        ibu: $("#ibu").val().trim(),
        yld: $("#yield").val().trim(),
        description: $("#description").val().trim(),
        ingredients: ingreds,
        instructions: $("#directions").val().trim()
    };

   $.ajax({
        type: "POST",
        url: "/recipes/new",
        contentType: "application/json",
        data: JSON.stringify(recipe),
        dataType: "json"
    }).done(function(data){
        console.log(data);
        window.location = "/recipes";
    });

//    console.log(recipe);

});

$("#parse-ingredients").on("click", function(event) {
    event.preventDefault();
    $(".table").removeClass("hidden");
    var ingredHash = $("#ingredients").val().trim();
    var ingredArr = ingredHash.split("\n")
    for (var i=0; i < ingredArr.length; i++) {
        var curLine = ingredArr[i].split(" ");
        var quant = curLine[0];
        var unit = curLine[1];
        var descrip = curLine.slice(2).join(" ");
        createNewLine(quant, unit, descrip);
    }
    $("#ingred-paste").hide();

});

function createNewLine(q, u, d) {
    var newRow = $("<tr>")
    newRow.append("<td contenteditable='true' class='quant'>" + q + "</td>");
    newRow.append("<td contenteditable='true' class='unit'>" + u + "</td>");
    newRow.append("<td contenteditable='true' class='descrip'>" + d + "</td>");
    $("#ingred-rows").append(newRow);
};

$(".edit-rec").on("click", function(event) {
    event.preventDefault();
    var id = $(this).data("id");
    window.location = "/recipes/edit/" + id;
})

