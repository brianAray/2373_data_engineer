## Exercise 2

Find out how much RAM and how many cores do you have on your system. My system has 16GB of RAM and a 4-Core CPU.

You want to run a Spark job that processes a medium-sized CSV file. You want to ensure you leave at least 4GB of RAM for your OS and other apps (Chrome, VS Code).

**Your Tasks:**

Write the `spark-submit` command for this local job that meets these requirements:

- Uses 2/3 of Cores out of the available cores.
- Sets the **Driver Memory** to half of your available RAM.
- Sets a custom name for the job: `"Production_Test_Run"`.
- Includes a configuration to set `spark.sql.shuffle.partitions` to have 2 tasks per core (If you are using 6 cores then 12 partitions, 2 tasks per core is a good rule of thumb).
- Points to your sensor processing python file.