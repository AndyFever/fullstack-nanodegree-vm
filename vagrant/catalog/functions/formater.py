def format_text(text):
    """Returns the text in a format ready for markdown"""

    tags = [["<strong>", "**"], ["</strong>", "**"],
            ["<em>", "_"], ["</em>", "_"],
            ["<del>", "~~"], ["</del>", "~~"]]

    formated_text = ""

    # Replace all the formating tags with markdown
    for tag in tags:
        if tag[0] in text:
            text = text.replace(tag[0], tag[1])

    # Replace the styling tag with a new line
    lines = text.split("<br>")

    for line in lines:
        line = line + "\n\n"
        formated_text += line
    return formated_text
