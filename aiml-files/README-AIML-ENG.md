# Additional AIML files in English

Please download the AIML files in English from the Free-AIML GitHub project:

👉 **[Open Free-AIML project](https://github.com/pandorabots/Free-AIML)**

Place them inside the _dati/aiml/EN/ directory.
When English is selected, the assistant will automatically use these files.

---

## Notes

The attributes inside the `template` tag are proprietary extensions of **myAssistente**.
Add them to the standard file to specify:
- wich assistant avatar will be displayed
- wich command myAssistente shuould run
- wich lateral panel should be open (1) /closed (0)
If the attribute avatar is omitted, one of the avatars defined in the `config.json` file will be selected at random.

Other AIML parsers will simply ignore this attribute.

---

### Example

       <template avatar="positivo" comando="apri posta"  menu="0010">
---