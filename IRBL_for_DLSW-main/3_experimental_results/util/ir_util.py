
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial import distance

def retrieval_bm25(bm25, file_indexes,  query):    
    tokenized_query = query.split(" ")    
    doc_scores = bm25.get_scores(tokenized_query)
    file_score_dict = {}
    for i in range(len(doc_scores)):
        file_index = file_indexes[i]
        file_score = doc_scores[i]
        file_score_dict[file_index] = file_score

    return file_score_dict

def retrieval_bm25_revised(bm25, file_indexes, query, length_score_dict):
    tokenized_query = query.split(" ")    
    doc_scores = bm25.get_scores(tokenized_query)
    file_score_dict = {}
    for i in range(len(doc_scores)):
        file_index = file_indexes[i]
        length_score = length_score_dict[file_index]
        file_score = doc_scores[i] * length_score
        file_score_dict[file_index] = file_score

    return file_score_dict


def retrieval_tfidf(vectorizer, file_tfidf, file_indexes, query):
    query_tfidf = vectorizer.transform([query])
    sim_scores = cosine_similarity(query_tfidf, file_tfidf).flatten()
    file_score_dict = {}
    for i in range(len(file_indexes)):
        file_index = file_indexes[i]
        file_score = sim_scores[i]
        file_score_dict[file_index] = file_score
    return file_score_dict

def retrieval_tfidf_revised(vectorizer, file_tfidf, file_indexes, query, length_score_dict):
    query_tfidf = vectorizer.transform([query])
    sim_scores = cosine_similarity(query_tfidf, file_tfidf).flatten()
    file_score_dict = {}
    for i in range(len(file_indexes)):        
        file_index = file_indexes[i]
        file_score = sim_scores[i]        
        length_score = length_score_dict[file_index]
        file_score = file_score * length_score
        file_score_dict[file_index] = file_score

    return file_score_dict

def retrieval_lsi(dictionary, lsi, index, file_indexes, query):

    vec_bow = dictionary.doc2bow(query.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    sims = index[vec_lsi]              
    
    file_score_dict = {}
    for i in range(len(sims)):
        file_index = file_indexes[i]
        file_score = sims[i]
        file_score_dict[file_index] = file_score

    return file_score_dict

def retrieval_jsm(documents_term_prob_matrix, file_indexes, query_term_prob_list):
    
    ind = 0
    file_score_dict = {}
    for doc_probs in documents_term_prob_matrix:
        score = distance.jensenshannon(doc_probs,query_term_prob_list)
        file_id = file_indexes[ind]
        ind += 1
        file_score_dict[file_id] = 1- score
    return file_score_dict


# for JSM
def get_doc_term_probs_jsm(files_corpus):  
    cnt_vectorizer = CountVectorizer(max_features=10000)
    X = cnt_vectorizer.fit_transform(files_corpus)
    X_terms = cnt_vectorizer.get_feature_names()
        
    doc_cnt_matrix = X.toarray()
    term_prob_matrix = []
    for doc in doc_cnt_matrix:
        all_terms = sum(doc)
        new_doc = []
        for cnt in doc:
            value = 0
            if cnt != 0:
                value = cnt / all_terms
            new_doc.append(value)
        term_prob_matrix.append(new_doc)
    return cnt_vectorizer, term_prob_matrix

def get_query_term_probs_jsm(cnt_vectorizer, query):
    X_query = cnt_vectorizer.transform([query])
    query_cnt = X_query.toarray()[0]
    all_terms_query = sum(query_cnt)
    new_query_cnt = []
    for cnt in query_cnt:
        value = 0
        if cnt != 0:
            value = cnt / all_terms_query
        new_query_cnt.append(value)
    return new_query_cnt


def evaluation(sim_scores, gtf_list, files_num, num_top_index):
    sim_scores_sort = sorted(sim_scores.items(), reverse=True, key=lambda item: item[1])
    rank = 1
    top_rank = files_num
    rr = 0
    ap = 0
    find_bug_num = 0
    non_buggy_file_indexes = []
    top_file_indexes = []
    for key, _ in sim_scores_sort:
        if len(gtf_list) == find_bug_num and len(top_file_indexes) == num_top_index:
            break
        if key in gtf_list:
            find_bug_num += 1
            if rr == 0:
                rr = 1.0 / rank
                top_rank = rank
            ap += find_bug_num / rank
        if len(non_buggy_file_indexes) < 10:
            non_buggy_file_indexes.append(key)
        if rank < num_top_index:
            top_file_indexes.append(key)
        rank += 1
    if find_bug_num > 0:
        ap = ap / find_bug_num
    return top_rank, rr, ap, non_buggy_file_indexes, top_file_indexes

    
def evaluation_wt_bfids(sim_scores, gtf_list, files_num, num_top_index):
    sim_scores_sort = sorted(sim_scores.items(), reverse=True, key=lambda item: item[1])
    rank = 1
    top_rank = files_num
    rr = 0
    ap = 0
    find_bug_num = 0
    non_buggy_file_indexes = []
    top_file_indexes = []
    top_buggy_file_ids = []
    for key, _ in sim_scores_sort:
        if len(gtf_list) == find_bug_num and len(top_file_indexes) == num_top_index:
            break
        if key in gtf_list:
            find_bug_num += 1
            if rr == 0:
                rr = 1.0 / rank
                top_rank = rank
            ap += find_bug_num / rank
            top_buggy_file_ids.append(key+":"+str(rank))
        if len(non_buggy_file_indexes) < 10:
            non_buggy_file_indexes.append(key)
        if rank < num_top_index:
            top_file_indexes.append(key)
        rank += 1
    if find_bug_num > 0:
        ap = ap / find_bug_num
    return top_rank, rr, ap, non_buggy_file_indexes, top_file_indexes, top_buggy_file_ids