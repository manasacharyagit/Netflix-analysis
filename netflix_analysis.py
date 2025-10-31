import streamlit as st;
import pandas as pd;

st.set_page_config(page_title="Netflix Movies", layout="wide")
url = "https://raw.githubusercontent.com/manasacharyagit/Netflix-analysis/refs/heads/master/mymoviedb.csv"
df = pd.read_csv(url, lineterminator='\n')


st.title("🎬 Netflix Movie List")


st.write("Total unique movies:", len(df))

# ----------------------------Creating Verdict column--------------------------------
def categorize_verdict(df,col, labels):
    desc  = df[col].describe()
    bins = [desc['min'], desc['25%'], desc['50%'], desc['75%'], desc['max']]
    df['Verdict'] = pd.cut(df[col], bins = bins, labels = labels, include_lowest=True)


labels = ["Poor", "Average", "Good", "Excellent"]
categorize_verdict(df, "Vote_Average", labels)

# Genre Filter ----------------------------------------------------------------------
search = st.text_input("🔍 Search Movie")
all_genres = sorted(
    set(g.strip() for sublist in df['Genre'].dropna().str.split(',') for g in sublist)
)


selected_genre = st.selectbox("🎬 Select Genre", ["All"]+all_genres)
if selected_genre =="All":
    filtered_df = df
else:
    filtered_df = df[df['Genre'].apply(
        lambda x: any(g.strip().lower() == selected_genre.strip().lower() for g in str(x).split(','))
    )]
if search:
    filtered_df = filtered_df[filtered_df['Title'].str.contains(search, case=False, na=False)]
     
movies = filtered_df.drop_duplicates(subset=['Title'])

# -----------------------------pagination setting --------------------------------------
movies_per_page = 30
total_movies = len(movies)
total_pages = total_movies // movies_per_page + (total_movies % movies_per_page>0)

# Track the current page in session state
if"page" not in st.session_state:
    st.session_state.page = 1

# Navigation control
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("⬅️ Previous") and st.session_state.page>1:
        st.session_state.page -=1
with col3:
    if st.button("Next ➡️") and st.session_state.page<total_pages:
        st.session_state.page +=1
# Display current page number
st.write(f"Page {st.session_state.page} of {total_pages}")

# Calculate which movies to show
start_idx = (st.session_state.page-1) * movies_per_page
end_idx = start_idx + movies_per_page
page_movies = movies.iloc[start_idx:end_idx]

st.subheader("All the movies")
st.write(f"Selected Genre: **{selected_genre}**", " | "f"Total Movies: **{len(movies)}**")

# -----------------------------------Movies list-----------------------------------------

@st.dialog("🎬 Movie Details")
def show_movie_details(selected):
    

    st.subheader(f"🎬 {selected['Title']}")
    st.write(f"**Release Date:** {selected['Release_Date']}")
    st.write(f"**Genre:** {selected['Genre']}")
    st.write(f"**Vote Average:** {selected['Vote_Average']}")
    st.write(f"**Verdict:** {selected['Verdict']}")
    st.image(selected['Poster_Url'], width=500)
movies_per_row = 5
for i in range(0, len(page_movies), movies_per_row):
    cols = st.columns(movies_per_row)
    for j, col in enumerate(cols):
        if i+j<len(page_movies):
            movie = page_movies.iloc[i+j]
            with col:
                if st.button(movie['Title'], key=movie['Title']):
                    st.session_state['selected_movie'] = movie['Title']
                    show_movie_details(movie)
# ----------------------------------Movie details----------------------------------------




    






st.write("Project made by Manas Acharya")

