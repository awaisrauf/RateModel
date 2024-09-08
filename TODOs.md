# TODOs

- [ ] Add restart button that takes you back to intial point
- [ ] Add session based stuff
- [ ] Remvoe global variable
- [ ] Error: if you reload after completing ratings, it throws error of index out of range

```bash
File "rate_model_output/app.py", line 70, in index
    if request.method == 'POST':
        preference = request.form.get('preference')
        if not preference:
            return "No preference selected", 400
 
        current_question = questions[question_id]
        save_rating(preference, current_question['question_id'])
        question_id += 1
        get_next_question_id.current_question_id = question_id
 
        if question_id >= len(questions):
IndexError: list index out of range
```
