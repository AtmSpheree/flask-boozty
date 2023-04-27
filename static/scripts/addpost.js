const LOCAL_STORAGE_IS_OPENED_KEY = "is-post-opened";
const LOCAL_STORAGE_ERRORS_KEY = "form-errors";

const LOCAL_META_DATA_IS_OPENED = JSON.parse(
  localStorage.getItem(LOCAL_STORAGE_IS_OPENED_KEY)
);
const LOCAL_META_DATA_ERRORS = JSON.parse(
  localStorage.getItem(LOCAL_STORAGE_ERRORS_KEY)
);

let isOpened = LOCAL_META_DATA_IS_OPENED && LOCAL_META_DATA_IS_OPENED.isOpened;

if (LOCAL_META_DATA_ERRORS.length != 0) {
  var errors = LOCAL_META_DATA_ERRORS;
} else {
  var errors = Array();
}

let form_checkbox = document.getElementById("is_opened");
if (isOpened) {
  form_checkbox.checked = true;
} else {
  form_checkbox.checked = false;
  renderUsersBlock();
}
if (errors) {
  for (index = 0; index < errors.length; index++) {
    let element = document.getElementById(errors[index]["child_id"]);
    let parent = findParentBySelector(element, "h5");
    console.log(element, parent);
    renderFormErrorAfterElement(parent, errors[index]["message"]);
  }
}

function changeFormCheckboxIsOpened() {
  isOpened = !isOpened;
  const META = { isOpened };
  localStorage.setItem(LOCAL_STORAGE_IS_OPENED_KEY, JSON.stringify(META));
  renderUsersBlock();
}

function submitAddPostForm() {
  let errors_temp = Array();
  json_file = JSON.parse(
    document.getElementById("stuff").innerHTML.replace(/&#34;/gi, '"')
  );

  let form = document.forms.form;
  let files_count = form.elements.files.files.length;
  let allowed_extensions = json_file["ALLOWED_EXTENSIONS_FILES"];

  for (index = 0; index < files_count; index++) {
    let f1 = false;
    for (index_2 = 0; index_2 < allowed_extensions.length; index_2++) {
      if (
        endsWith(
          form.elements.files.files[index].name,
          allowed_extensions[index_2].toLowerCase()
        )
      ) {
        f1 = true;
      }
    }
    if (!f1) {
      let message =
        "Вы можете загружать файлы только с допустимыми расширениями. ";
      message += "(" + allowed_extensions.join(", ") + ")";
      let object = { child_id: "files", message: message };
      errors_temp.push(object);
    }
  }

  if (files_count > json_file["MAX_FILES_COUNT"]) {
    let message =
      "Вы можете загружать не больше " +
      json_file["MAX_FILES_COUNT"] +
      " файлов в одной записи.";
    let object = { child_id: "files", message: message };
    errors_temp.push(object);
  }

  let labels = document.getElementsByTagName("LABEL");
  for (let i = 0; i < labels.length; i++) {
    if (labels[i].htmlFor != "") {
      let elem = document.getElementById(labels[i].htmlFor);
      if (elem) {
        if (elem.hasAttribute("label")) {
          elem.label.push(labels[i]);
        } else {
          elem.label = Array(labels[i]);
        }
      }
    }
  }

  let tags_block = document.getElementById("tags_block");
  let tags = Array();
  for (index = 0; index < tags_block.children.length; index++) {
    if (tags_block.children[index].nodeName == "INPUT") {
      if (tags_block.children[index].checked) {
        for (
          index_2 = 0;
          index_2 < tags_block.children[index].label.length;
          index_2++
        ) {
          if (
            tags_block.children[index].label[index_2].getAttribute("name") ==
            "tag_name"
          ) {
            tags.push(tags_block.children[index].label[index_2].innerHTML);
          }
        }
      }
    }
  }
  let tags_input = document.getElementById("tags");
  tags_input.value = tags.join(", ");

  let users_block = document.getElementById("users_block");
  let users = Array();
  f1 = false;
  for (index = 0; index < users_block.children.length; index++) {
    if (users_block.children[index].nodeName == "INPUT") {
      if (users_block.children[index].checked) {
        f1 = true;
        for (
          index_2 = 0;
          index_2 < users_block.children[index].label.length;
          index_2++
        ) {
          if (
            users_block.children[index].label[index_2].getAttribute("name") ==
            "user_email"
          ) {
            users.push(users_block.children[index].label[index_2].innerHTML);
          }
        }
      }
    }
  }
  if (users_block.children.length != 0 && !isOpened && !f1) {
    let message =
      "Чтобы опубликовать закрытую запись, выберите, кому она будет доступна.";
    let object = { child_id: "invited_users", message: message };
    errors_temp.push(object);
  }
  let invited_users_input = document.getElementById("invited_users");
  invited_users_input.value = users.join(", ");

  localStorage.setItem(LOCAL_STORAGE_ERRORS_KEY, JSON.stringify(errors_temp));
  document.form.submit();
}

function getAllUsers() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/api/user", false);
  xhr.send();
  let data = xhr.responseText;
  return data;
}

function renderUsersBlock() {
  json_file = JSON.parse(
    document.getElementById("stuff").innerHTML.replace(/&#34;/gi, '"')
  );
  let checkbox = document.getElementById("is_opened");
  let users_block = document.getElementById("users_block");
  let users_block_text = document.getElementById("users_block_text");
  let current_user_email = document.getElementById("current_user_email");
  let users = getAllUsers();
  users = JSON.parse(users);
  if (checkbox.checked) {
    users_block.style.display = "none";
    users_block.innerHTML = "";
    users_block_text.style.display = "none";
    users_block_text.innerHTML = "";
  } else {
    users_block.style.display = "block";
    users_block_text.style.display = "block";
    users_block_text.innerHTML =
      "Выберите пользователей, которым будет доступна запись:";
    for (index = 0; index < users["users"].length; index++) {
      let user = users["users"][index];
      if (current_user_email.getAttribute("value")) {
        if (user["email"] == current_user_email.getAttribute("value")) {
          continue;
        }
      }

      let input = document.createElement("input");
      input.className = "btn-check";
      input.id = "btncheck" + String(index + 1);
      input.setAttribute("type", "checkbox");
      input.setAttribute("autocomplete", "off");
      users_block.appendChild(input);

      let label_div = document.createElement("label");
      label_div.setAttribute("for", "btncheck" + String(index + 1));
      label_div.className =
        "btn btn-outline-secondary d-flex align-items-center justify-content-center";

      let img = document.createElement("img");
      img.className = "avatar_mini_2 rounded-circle img-fluid me-1";
      if (user["avatar"] == "") {
        img.src = path.join(json_file["DEFAULT_PHOTOS_PATH"]);
      } else {
        img.src = path.join(
          json_file["UPLOAD_FOLDER_FOR_REQUEST"],
          json_file["UPLOAD_FOLDER_PHOTOS"],
          user["avatar"]
        );
      }
      label_div.appendChild(img);

      let label = document.createElement("label");
      label.innerText = user["nickname"];
      label_div.appendChild(label);

      users_block.appendChild(label_div);

      let label_2 = document.createElement("label");
      label_2.innerText = user["email"];
      label_2.style.display = "none";
      label_2.setAttribute("for", "btncheck" + String(index + 1));
      label_2.setAttribute("name", "user_email");
      users_block.appendChild(label_2);
    }
  }
}
