## Exercise 1

You will need to generate the data using this python script in the `data` folder `generate_sensor_data.py`

**The Scenario:**

You have a list of sensor readings in the format: `"SensorID,Temperature"`. Some readings are corrupted (non-numeric), and you want to calculate the average temperature per sensor while filtering out "Outlier" sensors using a blacklist.

**Your Tasks:**

1. **Shared Variables:** Create a **Broadcast variable** containing a set of blacklisted Sensor IDs: `{"SN_09", "SN_13"}`.
2. **Shared Variables:** Create an **Accumulator** to count how many corrupted rows were encountered.
3. **Transformations:** Parse the strings into Key-Value pairs `(SensorID, Temperature)`.
    - Filter out any sensors in the blacklist.
    - Handle errors using a `try/except` block that increments your accumulator.
4. **Action:** Use `reduceByKey` and `mapValues` to find the average for each sensor.  Be careful of `NaN`
5. **Output:** Print the final averages and the total count of corrupted rows.
6. Use the pause trick to view the process on the Spark UI