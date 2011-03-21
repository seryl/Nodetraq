$(document).ready(function() {
    $('#search_field').focus();
    });

function addGroups() {
  $('#available_groups option:selected').each(function() {
      $('#member_groups').prepend($(this));
    });
}

function delGroups() {
  $('#member_groups option:selected').each(function() {
      $('#available_groups').prepend($(this));
    });
}

function changePassword() {
  var username = $('meta[name=username]').attr('content');
  var password = $('#new_password').val();
  if (password == $('#confirm_password').val()) {
    if (password.length > 5) {
      window.location = '/users/change_password/' +
        username + '?password=' + password;
    } else {
      alert('Passwords must be at least 6 characters in length.');
    }
  } else {
    alert('Passwords do not match');
  }
}

function apply_group_function() {
  var selected = $("#function").val();
  this['run_' + selected]();
}

function renameUser() {
  var username = $('meta[name=username]').attr('content');
  $.ajax({
      url: '/users/rename_user/' + username,
      type: 'POST',
      data: {},
      success: function(data) {
        $.modal(data);
      }
  });
}

function enableUser() {
  var username = $('meta[name=username]').attr('content');
  window.location = '/users/enable_user/' + username;
}

function disableUser() {
  var username = $('meta[name=username]').attr('content');
  window.location = '/users/disable_user/' + username;
}

function deleteUser() {
  var username = $('meta[name=username]').attr('content');
  if (confirm("Are you sure you want to delete " + username + "?")) {
    window.location = '/users/delete_user/' + username;
  }
}

function resetPassword() {
  var username = $('meta[name=username]').attr('content');
  window.location = '/users/reset_password/' + username;
}

function submitChanges() {
  var username = $('meta[name=username]').attr('content');
  var uid = $('#uidnumber').val();
  var cn = $('#cn').val();
  var mail = $('#mail').val();
  var loginshell = $('#loginshell').val();
  var title = $('#title').val();
  var manager = $('#manager').val();
  var departmentNumber = $('#departmentnumber').val();
  var roomNumber = $('#roomnumber').val();
  var orgchartmanager = $('input:radio[name=orgchartmanager]:checked').val();
  var deploycode = $('input:radio[name=deploycode]:checked').val();
  var utilityaccount = $('input:radio[name=utilityaccount]:checked').val();

  var href = "/users/update/" + username + '?';
  href += 'uidNumber=' + uid;
  href += '&cn=' + cn;
  href += '&mail=' + encodeURIComponent(mail);
  href += '&loginShell=' + encodeURIComponent(loginshell);
  href += '&title=' + encodeURIComponent(title);
  href += '&manager=' + encodeURIComponent(manager);
  href += '&departmentNumber=' + encodeURIComponent(departmentNumber);
  href += '&roomNumber=' + encodeURIComponent(roomNumber);
  href += '&orgchartmanager=' + encodeURIComponent(orgchartmanager);
  href += '&deploycode=' + encodeURIComponent(deploycode);
  href += '&utilityaccount=' + encodeURIComponent(utilityaccount);

  $('#member_groups option').each(function() {
      href += '&group=' + $(this).val();
    });

  window.location = href;
}

function createUser() {
  if (verify_username()) {
    var username = $('#username').val();
    var name = $('#name').val();
    var mail = $('#mail').val();
    var loginshell = $('#loginshell').val();
    var title = $('#title').val();
    var manager = $('#manager').val();
    var departmentNumber = $('#departmentnumber').val();
    var roomNumber = $('#roomnumber').val();
    var orgchartmanager = $('input:radio[name=orgchartmanager]:checked').val();
    var deploycode = $('input:radio[name=deploycode]:checked').val();
    var utilityaccount = $('input:radio[name=utilityaccount]:checked').val();

    var href = "/users/create";
    href += '?username=' + username;
    href += '&name=' + encodeURIComponent(name);
    href += '&mail=' + encodeURIComponent(mail);
    href += '&loginShell=' + encodeURIComponent(loginshell);
    href += '&title=' + encodeURIComponent(title);
    href += '&manager=' + encodeURIComponent(manager);
    href += '&departmentNumber=' + encodeURIComponent(departmentNumber);
    href += '&roomNumber=' + encodeURIComponent(roomNumber);
    href += '&orgchartmanager=' + encodeURIComponent(orgchartmanager);
    href += '&deploycode=' + encodeURIComponent(deploycode);
    href += '&utilityaccount=' + encodeURIComponent(utilityaccount);

    $('#member_groups option').each(function() {
        href += '&group=' + $(this).val();
        });

    window.location = href;
  }
}

function update_search() {
    var selected_search = $("input[name=search_type]:checked").val();
    if (selected_search == 'users') {
        $("#search_form").attr("action", "/users");
    } else {
        $("#search_form").attr("action", "/users/" + selected_search);
    }
}

function verify_username() {
    re = /^\w+\.\w+$/;
    if (re.test($("#username").val())) {
        return true;
    } else {
        alert('Username doesn\'t follow firstname.lastname convention.');
        $("#username").focus();
        return false;
    }
}

function update_shown_attrib() {
  var selection = $("#attributes_selections").val();
  $("#orgchartmanager_div").css('display', 'none');
  $("#deploycode_div").css('display', 'none');
  $("#utilityaccount_div").css('display', 'none');
  if (selection) {
    $("#"+selection).css('display', 'block');
  }
}

function submitGroupChanges() {
  var group = $('#group').val();
  var cn = $('#cn').val();
  var description = $('#description').val();
  var href = '/users/updategroup/' + group + '?';

  href += '&cn=' + encodeURIComponent(cn);
  href += '&description=' + encodeURIComponent(description);

  window.location = href;
}

function run_remove_group_member() {
  var group = $('meta[name="group"]').attr('content');
  var members = new Array();
  var href = '/users/' + group + '/members';

  $(".list input[type='checkbox']:checked")
    .each(function() {
        members.push($(this).attr('name'));
      });

  $.ajax({
      url: '/users/' + group + '/remove_members',
      type: "POST",
      data: JSON.stringify({'members': members}),
      success: function(data) {
        window.location = href;
      }
    });
}