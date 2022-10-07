import streamlit as st
import requests
import os
access_token = st.secrets['access_token']

#os.system('git config --global user.email "spiruel@gmail.com"')
#os.system('git config --global user.name "Samuel Bancroft"')

good = False

def check_website_url(url):
	if 'http' not in url:
		return 404
	else:
		r = requests.get(f'{url}')
		return r.status_code
	
def check_github_user(user):
	r = requests.get(f'https://api.github.com/users/{user}')
	return r.status_code
	

def check_twitter_user(user):
	r = requests.get(f'https://twitter.com/{user}')
	st.write(r.text)
	if 'This account doesn’t exist' in r.text:
		return 404
	else:
		return 200
	
st.header('Submit your profile to sciml-leeds.github.io')

st.subheader('Example submission:')
st.text("""

- name: Samuel Bancroft
  social:
    website: https://environment.leeds.ac.uk/see/pgr/9458/samuel-bancroft
    github: spiruel
    twitter: spiruel
  techniques:
    - Semi-supervised/self-supervised learning
    - convolutional networks
  applications:
    - crop type classification
    - satellite time series classification
    - crop yield estimation
    """)
    
with st.form("form"):
	name = st.text_input('Name:')
	
	st.write('---')
	
	st.caption('Socials')
	
	website = st.text_input('Website URL (include https)')
	github = st.text_input('Github username')
	twitter = st.text_input('Twitter username')

	st.write('---')
	
	st.caption('List up to three techniques in your research:')
	
	techniques = []
	for i in range(3):
		t = st.text_input('', key=str(i), help='e.g. convolutional neural networks').capitalize()
		techniques.append(t)
	
	st.write('---')
	
	st.caption('List up to three applications in your research:')
	
	applications = []
	for i in range(3):
		a = st.text_input('', key=str(i)+'_', help='e.g. crop type classification')
		applications.append(a)
	
	st.write('---')
	
	image = st.file_uploader('Profile picture', type=['png', 'jpg', 'jpeg'])
	
	submitted = st.form_submit_button("Does everything look correct? Now click here")
	
	if submitted:
	
		good = True
		if len(name) <= 1:
		       st.error('Invalid name')
		       good = False
		if check_website_url(website) == 404:
			st.error('Could not find website from given URL')
			good = False
		if check_github_user(github) != 200:
			st.error(f'Github username {github} does not exist')
			good = False
		#if check_twitter_user(twitter) is not 200:
		#	st.error(f'Twitter username {twitter} does not exist')
		#	good = False
			
		techniques = [j.capitalize() if i == 0 else j.lower() for i,j in enumerate(techniques)]
		applications = [j.capitalize() if i == 0 else j.lower() for i,j in enumerate(applications)]
		
		techniques_list = '\n'.join(['    '*j + '- ' + i for j,i in enumerate(techniques)])
		applications_list = '\n'.join(['    '*j + '- ' + i for j,i in enumerate(applications)])
		
		if good:
			new_text = f"""
- name: {name.title()}		
  social:
    website: {website}
    github: {github}
    twitter: {twitter}
  techniques:
    {techniques_list}
  applications:
    {applications_list}
				    """
			st.text(new_text)

			if image:
				st.image(image)
				
			name_trunc = name.replace(' ', '').lower()
			cwd = os.getcwd()
			os.system('rm -rf --interactive=never sciml-leeds.github.io')
			os.system('git clone https://{access_token}@github.com/sciml-leeds/sciml-leeds.github.io.git')
			os.chdir('sciml-leeds.github.io')
			os.system('git fetch')
			os.system(f"git checkout -b {name_trunc}")
			
			with open('_data/people.yaml', 'a') as f:
				f.write(new_text)
				
			os.system("git add '_data/people.yaml'")

			if image is not None:
				with open(f"assets/img/{name_trunc}.png","wb") as f: 
      					f.write(image.getbuffer())
				st.info('Added image')
				os.system(f"git add 'assets/img/{name_trunc}.png'")
				
			os.system("git commit -m'initial commit'")
			os.system(f"git remote set-url origin https://{access_token}@github.com/sciml-leeds/sciml-leeds.github.io.git")
			os.system(f'git push --set-upstream origin {name_trunc}')
			#os.system(f"git push")
			os.chdir(cwd)
					
			st.success('Submitted branch to gh')

