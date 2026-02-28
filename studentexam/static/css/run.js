<script>
        var endTime = new Date("{{ end_time }}");
        function updateTimer() {
            var currentTime = new Date();
            var timeLeft = endTime - currentTime;

            if (timeLeft <= 0) {
                document.getElementById("timer").textContent = "Time's up!";
                clearInterval(timerInterval);
            } else {
                var hours = Math.floor(timeLeft / 3600000);
                var minutes = Math.floor((timeLeft % 3600000) / 60000);
                var seconds = Math.floor((timeLeft % 60000) / 1000);

                document.getElementById("timer").textContent = "Time left: " + hours + "h " + minutes + "m " + seconds + "s";
            }
        }

        updateTimer();  // Call once to display the initial time
        var timerInterval = setInterval(updateTimer, 1000);  // Update the timer every second
    </script>