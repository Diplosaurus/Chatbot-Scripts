# Wish
This is a Script inspired by the Wish system in Genshin Impact. It allows a stream member to perform pulls on the event banner using their channel points.

## Usage
`!wish <points>`

- Points are used to pay for the roll. The cost is determined by the Streamer's settings. To use this command, put in the number of points you wish to use. The script will calculate how many rolls you can do and deduct them once the result is returned. 
- If a user puts in a point value that is higher than what they currently have, nothing will happen. 

## Streamer Setup
1. First, you'll need to download and import the script (See instructions [here](../README.md#how-to-download-and-install-a-script)).
2. Configure the following wish settings (optional):
    - Event Five Star: whatever character you want to be the featured five star. ex. 'Zhongli (Geo)'
    - Event Four Stars: A list of featured four star characters, separated by commas. ex. Razor (Electro), Lisa (Electro), Kaeya (Electro)
    - Additional Four Stars: A list of four stars to be included in the pool in addition to the default pool. If not specified, the default pool will remain the same.
    - Cost (optional): The amount of points per wish. If not provided, the the default of 160 will be used
    - Max Wishes: The amount of wishes a user can use at once. Default is 10.
3. Once finished, hit 'Save Settings'
4. Enable the script by checking the checkbox on the right
5. You're all set! Test it out by using the console!