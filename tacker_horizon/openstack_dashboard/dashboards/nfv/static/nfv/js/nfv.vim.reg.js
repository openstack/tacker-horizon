$( document ).ready(function() {
  var vim_type = $("#id_vim_type").find(":selected").first().text();
  toggle_vim_fields(vim_type);
  $("#id_vim_type").change(function(){
    vim_type = $("#id_vim_type").find(":selected").first().text();
    toggle_vim_fields(vim_type);
  });
});

function toggle_vim_fields(vim_type) {
  if (vim_type === 'OpenStack') {
    $("#id_username").closest(".form-group").show();
    $("#id_password").closest(".form-group").show();
    $("#id_password").val("");
    $("#id_domain_name").closest(".form-group").show();
    $("#id_ssl_ca_cert").closest(".form-group").hide();
    $("#id_bearer_token").val("None");
    $("#id_bearer_token").closest(".form-group").hide();
    $("input[name='auth_method']").closest(".form-group").hide();
    $("input[name='cert_verify']").closest(".form-group").show();
  } else if (vim_type === 'Kubernetes') {
    $("#id_domain_name").closest(".form-group").hide();
    $("input[name='cert_verify']").closest(".form-group").hide();
    $("#id_ssl_ca_cert").closest(".form-group").show();
    $("#id_bearer_token").closest(".form-group").show();
    $("#id_bearer_token").val("");
    $("input[name='auth_method']").closest(".form-group").show();
    var auth_method = $("input[name='auth_method']:checked").val();
    toggle_auth_fields(auth_method);
    $("input[name='auth_method']").change(function() {
      toggle_auth_fields(this.value);
    });
  }
}

function toggle_auth_fields(auth_method) {
  if (auth_method === 'basic') {
    $("#id_username").closest(".form-group").show();
    $("#id_password").closest(".form-group").show();
    $("#id_password").val("");
    $("#id_bearer_token").val("None");
    $("#id_bearer_token").closest(".form-group").hide();
  } else if (auth_method === 'bearer_token') {
    $("#id_bearer_token").closest(".form-group").show();
    $("#id_bearer_token").val("");
    $("#id_username").closest(".form-group").hide();
    $("#id_password").val("None");
    $("#id_password").closest(".form-group").hide();
  }
}
