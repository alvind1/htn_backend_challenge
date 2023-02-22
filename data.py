class Users:
  @staticmethod
  def parse_users(users:list)->dict:
    user_dict = {}
    for user in users:
      user_id, name, company, email, phone, _, skill, rating = user
      if user_id in user_dict:
        user_dict[user_id]['skills'].append({'skill': skill, 'rating': rating})
      else:
        user_dict[user_id] = {
          'id': user_id,
          'name': name,
          'company': company,
          'email': email,
          'phone': phone,
          'skills': []
        }
        if skill != None:
          user_dict[user_id]['skills'].append(
            {
              'skill': skill,
              'rating': rating
            }
          )
    return user_dict
  
  @staticmethod
  def parse_put_request(queries:dict)->dict:
    args = ["name", "company", "email", "phone", "skills"]

    parsed_request = {}
    for arg in args:
      if arg in queries:
        parsed_request[arg] = queries[arg]
    
    return parsed_request