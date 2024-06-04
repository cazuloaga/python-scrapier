def parse_post_prompt_links(html_text: str, links: list = []):
  """
  Generates a prompt to extract a link to a post from HTML text.

  Parameters:
  - html_text (str): The HTML text containing the post information.
  - links (list): A list of links or relative path related to the post (optional).

  Returns:
  - prompt (str): A formatted prompt instructing to extract the link to the post.

  Note:
  - The html_text parameter should contain the HTML content with the post information.
  - The prompt generated by this function is intended to be clear and precise, minimizing the risk of errors
    or misunderstandings by those executing the task. However, the effectiveness of the prompt can vary based
    on the complexity of the HTML text provided and the familiarity of the task executor with JSON formatting.
  - This function does not parse the HTML or validate the resulting link itself; it merely prepares
    the instruction set for someone else to perform the conversion.
  - If links are provided, the prompt includes them as options for the link extraction.
  """
  if links:
    prompt = f"Extract the link to the post from the following HTML text below. Don't make up links, it should be either one from this list {str(links)}. ONLY RETURN A LINK OR A RELATIVE PATH. Make sure all the information is correct.\n"
  else:
    prompt = "Extract the link to the post from the following HTML text below. Don't make up links. ONLY RETURN A LINK OR A RELATIVE PATH. Make sure all the information is correct.\n"
  prompt += "###HTML TEXT###: \n\n" + html_text
  return prompt

def parse_post_prompt(html_text: str, relevance: str):
    """
    Prepares a prompt instructing to convert HTML text into a JSON object with specific keys.
    
    Parameters:
    - html_text (str): The HTML text that needs to be converted into a JSON object format.

    Returns:
    - str: A string containing the generated prompt. The prompt includes instructions for how to format
           the HTML text into a JSON object, specifying the required keys and the format for 'publication_date'.
           The actual HTML text to be converted is appended after the instruction.

    Note:
    - The function is designed to generate prompts for tasks involving data conversion or extraction from HTML
      content. It can be used in contexts where manual intervention, such as through crowdsourcing platforms, is
      required to parse and convert HTML into structured data.
    - The prompt generated by this function is intended to be clear and precise, minimizing the risk of errors
      or misunderstandings by those executing the task. However, the effectiveness of the prompt can vary based
      on the complexity of the HTML text provided and the familiarity of the task executor with JSON formatting.
    - This function does not parse the HTML or validate the resulting JSON object itself; it merely prepares
      the instruction set for someone else to perform the conversion.
    """
    prompt = "You will be given a post text. You will also be given a phrase. Is the phrase specifically found in the post text? Return a JSON object with 3 keys ('summary', 'relevance', and 'title'). The first key is 'summary' and it should contain a brief summary of the html text no more than 5 sentences long. The second key is 'relevance' and it should be depending on whether one of the phrases is in the html text, if the prase is in the html text it should provide a short one sentence justification that starts with 'The text mentions the phrase...', if the prase is NOT in the html text it should only contain 'This text does not appear to be relevant for you' nothing else. The third key is 'title' and it should be a brief 1 sentence tittle, no more than 15 words long, that suits the post text. Only return the JSON object. Be precise.\n\n"
    prompt += f"###POST TEXT###:\n{html_text}\n\n"
    prompt += f"#####Phrase#####:\n{relevance}"
    return prompt