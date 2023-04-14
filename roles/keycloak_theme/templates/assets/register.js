
function set_user_name() {
    let vorname = document.getElementById("firstName").value;
    let nachname = document.getElementById("lastName").value;
    if (vorname && vorname != '' && nachname && nachname != '')
    {
      let username = vorname.toLowerCase() + '.' + nachname.toLowerCase();
      let clean_username = username.replace(/[^\w\.]/gi, '')

      console.log(clean_username);
      document.getElementById("username").value = clean_username;
    }
}

function apply_rules(question){

  // find all corresponding rules
  let triggered_rules = rules.filter(rule => ('user.attributes.' + rule.triggered_by) == question.id);

  // check the rules whether trigger should be triggered
  for(let x in triggered_rules) {
    let rule = triggered_rules[x];

    rule.is_triggered = true;
    
    for(let y in rule.rules) {
      let trigger_rule = rule.rules[y];
      let id = 'user.attributes.' + trigger_rule.id;
      let element = document.getElementById(id);
      let value = element.value;

      if (element.type == "checkbox") {
        value = element.checked;
      }

      if (value != trigger_rule.value) {
        rule.is_triggered = false;
      }
    }
  }

  // reset every not triggered rule
  let reset_triggered_rules = triggered_rules.filter(rule => !rule.is_triggered);
  for (let x in reset_triggered_rules) {
    set_questions(reset_triggered_rules[x]);
  }

  // set every triggered rule
  let set_triggered_rules = triggered_rules.filter(rule => rule.is_triggered);
  for (let x in set_triggered_rules) {
    set_questions(set_triggered_rules[x]);
  }        
}

function set_questions(rule) {
  console.log(rule.is_triggered);
  
  let show_id = 'user.attributes.' + rule.show.form_item + ".div";
  console.log(show_id);        
  document.getElementById(show_id).classList.add("invisible");

  if(rule.is_triggered) 
    document.getElementById(show_id).classList.remove("invisible");

  if(rule.show.options) {
    for (let z in rule.show.options) {
      let option = rule.show.options[z]
      let option_id = 'user.attributes.' + rule.show.form_item + "." + option;

      document.getElementById(option_id).classList.add("hidden");
      if(rule.is_triggered) 
      
        document.getElementById(option_id).classList.remove("hidden");
    }
  }
}

function set_other(field, input, html_class) {
  console.log(input.value);
  if ( input.value == 'other' ) {
    let outerHTML = "<input type='text' " + 
      ((field.required == "True") ? 'required ' : '') + 
      "class='" + html_class + "' id='user.attributes." + 
      field.attribute + "' name='user.attributes." + 
      field.attribute + "'  placeholder='"+
      field.other + "' />";
    input.outerHTML = outerHTML;
  }
  else {
    let id = '#' + input.value;
    $(id).removeClass("hidden");
  }      
}

var currentTab = 1; // Current tab is set to be the first tab (0)

function validateForm() {
  // This function deals with validation of the form fields
  var section, inputs, i, valid = true;
  section = document.getElementsByClassName("form-step");
  inputs = section[currentTab -1].querySelectorAll("[required]");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < inputs.length; i++) {
    // If a field is empty...
    if (inputs[i].value == "") {
      // add an "invalid" class to the field:
      inputs[i].classList.add("invalid")
      // and set the current valid status to false:
      valid = false;
    }
    else {
      inputs[i].classList.remove("invalid")
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementById("step-header-"+ currentTab).classList.add("finish");
  }
  return valid; // return the valid status
}

/**
 * Define a function to navigate betweens form steps.
 * It accepts one parameter. That is - step number.
 */
 const navigateToFormStep = (step) => {
    /**
     * Hide all form steps.
     */
    if (step == 1 && !validateForm ()) { 
      return false;
    }

    currentTab += step;
    
    console.log(currentTab)
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });
    /**
     * Mark all form steps as unfinished.
     */
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });
    /**
     * Show the current form step (as passed to the function).
     */
    document.querySelector("#step-" + currentTab).classList.remove("d-none");
    /**
     * Select the form step circle (progress bar).
     */
    const formStepCircle = document.querySelector('li[step="' + currentTab + '"]');
    /**
     * Mark the current form step as active.
     */
    formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
    formStepCircle.classList.add("form-stepper-active");
    /**
     * Loop through each form step circles.
     * This loop will continue up to the current step number.
     * Example: If the current step is 3,
     * then the loop will perform operations for step 1 and 2.
     */
    for (let index = 0; index < currentTab; index++) {
        /**
         * Select the form step circle (progress bar).
         */
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        /**
         * Check if the element exist. If yes, then proceed.
         */
        if (formStepCircle) {
            /**
             * Mark the form step as completed.
             */
            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};