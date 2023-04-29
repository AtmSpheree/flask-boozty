let accessed_tags = JSON.parse(
  document.getElementById("accessed_tags").innerHTML.replace(/&#34;/gi, '"')
);
let tags_group = document.getElementById("tags_group");
for (index = 0; index < tags_group.children.length; index++) {
  if (accessed_tags) {
    if (tags_group.children[index].tagName.toLowerCase() == "input") {
      if (
        accessed_tags.indexOf(
          Number(tags_group.children[index].getAttribute("value"))
        ) != -1
      ) {
        tags_group.children[index].checked = true;
      } else {
        tags_group.children[index].checked = false;
      }
    }
  } else {
    if (tags_group.children[index].tagName.toLowerCase() == "label") {
      if (tags_group.children[index].innerHTML == "Все") {
        tags_group.children[index].checked = true;
      } else {
        tags_group.children[index].checked = false;
      }
    }
  }
}

function tagChange(object) {
  let tags_checked = Array();
  for (index = 0; index < tags_group.children.length; index++) {
    if (tags_group.children[index].tagName.toLowerCase() == "input") {
      if (tags_group.children[index].checked) {
        if (String(tags_group.children[index].getAttribute("value"))) {
          tags_checked.push(
            String(tags_group.children[index].getAttribute("value"))
          );
        }
      }
    }
  }
  if (tags_checked.length == 0) {
    object.checked = true;
    return;
  }
  if (object.checked) {
    if (object.getAttribute("value") == "0") {
      for (index = 0; index < tags_group.children.length; index++) {
        if (tags_group.children[index].tagName.toLowerCase() == "input") {
          if (tags_group.children[index].getAttribute("value") != "0") {
            tags_group.children[index].checked = false;
          }
        }
      }
      tags_checked = Array("0");
    } else {
      for (index = 0; index < tags_group.children.length; index++) {
        if (tags_group.children[index].tagName.toLowerCase() == "input") {
          if (tags_group.children[index].getAttribute("value") == "0") {
            tags_group.children[index].checked = false;
          }
        }
      }
    }
  }
  let new_tags_checked = Array();
  for (index = 0; index < tags_checked.length; index++) {
    if (tags_checked[index] != "0") {
      new_tags_checked.push(tags_checked[index]);
    }
  }
  new_tags_checked = new_tags_checked.join(";");
  document.location.href = "/?tags=" + new_tags_checked;
}
