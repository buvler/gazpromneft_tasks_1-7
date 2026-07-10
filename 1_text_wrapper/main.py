import textwrap

def format_text(text: str, max_length: int = 70) -> str:
    return textwrap.fill(text, width=max_length)

sample_text = (
    "Дан текст. Напишите программу, которая отформатирует этот текст так, чтобы в строке текста было не более 70 символов, а потом шел перенос строки. Слова при этом не должны разбиваться."
)

formatted_text = format_text(sample_text)
print(formatted_text)