function validateForm() {
            var formValid = true;
            var inputs = document.querySelectorAll("input");

            inputs.forEach(function(input) {
                if (input.value.trim() === "") {
                    formValid = false;
                }
            });

            if (!formValid) {
                document.getElementById("error-message").style.display = "block";
                return false;
                }
            
            return true;
        }