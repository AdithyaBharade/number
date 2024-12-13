from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def process_number(num):
    if len(num) > 10 or not num.isdigit():
        return "Invalid input. Please enter up to a 10-digit number."

    num = num.zfill(10)

    positions = {
        '3': (0, 0), '1': (0, 1), '9': (0, 2),
        '6': (1, 0), '7': (1, 1), '5': (1, 2),
        '2': (2, 0), '8': (2, 1), '4': (2, 2)
    }

    matrix = [['' for _ in range(3)] for _ in range(3)]

    for i, digit in enumerate(num):
        if digit in positions:
            row, col = positions[digit]
            if matrix[row][col]:
                matrix[row][col] += digit
            else:
                matrix[row][col] = digit
        elif digit == '0':
            for j in range(i - 1, -1, -1):
                if num[j] != '0':
                    row, col = positions[num[j]]
                    matrix[row][col] += '+'
                    break

    total = sum(int(digit) for digit in num) - 9
    while total > 9:
        total = sum(int(digit) for digit in str(total))

    total_position = positions[str(total)] if str(total) in positions else None
    if total_position:
        row, col = total_position
        if matrix[row][col]:
            matrix[row][col] += f"({total})"
        else:
            matrix[row][col] = f"({total})"

    fixed_width = 8
    output = "`\n"

    for i, row in enumerate(matrix):
        output += " | ".join(matrix[i][j].center(fixed_width) if matrix[i][j] else ' '.center(fixed_width) for j in range(3)) + "\n"
        if i < 2:
            output += "-" * (fixed_width * 3 + 6) + "\n"
    output += f"\nTotal = {total}\n"
    return output.strip()

def process_and_print_pyramid(number):
    digits = [int(d) for d in str(number)]

    if len(digits) > 10:
        return "Input must be a 10-digit number."

    pyramid_output = "\n"
    while len(digits) > 2:
        row = ""
        for i in range(len(digits)):
            row += str(digits[i])
            if i < len(digits) - 1:
                row += "+"
        pyramid_output += row + "\n"

        next_row = []
        for i in range(len(digits) - 1):
            sum_of_digits = digits[i] + digits[i + 1]
            if sum_of_digits > 9:
                sum_of_digits -= 9
            next_row.append(sum_of_digits)

        digits = next_row

    if len(digits) == 2:
        pyramid_output += f"{digits[0]}+{digits[1]}\nTotal = {digits[0] + digits[1]}\n"

    return pyramid_output.strip()

def process_number_pairs(num):
    if len(num) > 10 or not num.isdigit():
        return "Invalid input. Please enter a 10-digit number."
    
    very_good = {13, 31, 15, 51, 17, 71, 37, 73, 38, 83, 39, 93, 57, 75, 59, 95, 69, 96, 89, 98}
    good = {12, 21, 19, 91, 23, 32, 25, 52, 29, 92, 35, 53, 36, 63, 47, 74, 49, 94, 67, 76, 78, 87, 11, 22, 33, 44, 55, 66, 77, 88, 99}
    very_bad = {14, 41, 16, 61, 26, 62, 27, 72, 28, 82, 34, 43, 46, 64, 48, 84, 58, 85, 68, 96, 79, 97, 45, 54}
    bad = {18, 81, 24, 42, 56, 65}
    result = []
    i = 0

    while i < len(num) - 1:
        if num[i] == '0':
            i += 1
            continue
        j = i + 1
        while j < len(num) and num[j] == '0':
            j += 1
        if j < len(num):
            result.append(int(num[i] + num[j]))
        i = j

    categorized = {
        "Very Good": [],
        "Good": [],
        "Very Bad": [],
        "Bad": [],
    }

    for pair in result:
        if pair in good:
            categorized["Good"].append(pair)
        elif pair in very_good:
            categorized["Very Good"].append(pair)
        elif pair in bad:
            categorized["Bad"].append(pair)
        elif pair in very_bad:
            categorized["Very Bad"].append(pair)

    return result, categorized

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    name = request.form['name']
    phone_number = request.form['mobileNumber']
    
    if len(phone_number) != 10 or not phone_number.isdigit():
        error_message = "Invalid number. Please enter a valid 10-digit number."
        return render_template('index.html', error_message=error_message)

    matrix_output = process_number(phone_number)
    pyramid_output = process_and_print_pyramid(phone_number)
    pairs, categorized_pairs = process_number_pairs(phone_number)

    pair_colors = {}
    for pair in pairs:
        if pair in categorized_pairs["Very Good"]:
            pair_colors[pair] = "pair-very-good"
        elif pair in categorized_pairs["Good"]:
            pair_colors[pair] = "pair-good"
        elif pair in categorized_pairs["Bad"]:
            pair_colors[pair] = "pair-bad"
        elif pair in categorized_pairs["Very Bad"]:
            pair_colors[pair] = "pair-very-bad"

    return render_template('result.html', 
                           name=name,
                           phone_number=phone_number, 
                           matrix_output=matrix_output, 
                           pyramid_output=pyramid_output, 
                           pairs=pairs,
                           categorized_pairs=categorized_pairs,
                           pair_colors=pair_colors)

if __name__ == '__main__':
    app.run(debug=True)

