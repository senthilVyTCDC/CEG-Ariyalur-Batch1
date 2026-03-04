// Wait until page loads
document.addEventListener('DOMContentLoaded', function() {

    // DELETE confirmation (already exists)
    const deleteForms = document.querySelectorAll('form[action^="/delete/"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const confirmDelete = confirm("Are you sure you want to delete this card?");
            if (!confirmDelete) e.preventDefault();
        });
    });

    // Optional: Add/Edit form validation
    const cardForms = document.querySelectorAll('form:not([action^="/delete/"])');
    cardForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Example: check card number length
            const cardNumber = form.querySelector('input[name="card_number"]').value;
            if (cardNumber.length < 12) {
                alert("Card number must be at least 12 digits");
                e.preventDefault();
            }
        });
    });

});