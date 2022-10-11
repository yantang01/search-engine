import webdev
import os
import json
import searchdata


def parse_links(contents):
    start_index = 0
    end_index = 0
    start_tag = 'a href="'
    end_tag = '">'
    links = []
    while True:
        # get all the words in a list
        start_index = contents.find(start_tag, end_index)
        if start_index == -1:
            break
        end_index = contents.find(end_tag, start_index)
        # words is a list of all the words
        links.append(
            contents[(len(start_tag) + start_index):end_index])
    return links


def parse_words(contents):
    start_index = 0
    end_index = 0
    start_tag = '<p>'
    end_tag = '</p>'
    while True:
        # get all the words in a list
        start_index = contents.find(start_tag, end_index)
        if start_index == -1:
            break
        end_index = contents.find(end_tag, start_index)
        # words is a list of all the words
        words = contents[(len("<p>") + start_index):end_index].split()

    return words


def get_title(contents):
    start_tag = '<title>'
    end_tag = '</title>'
    start_index = contents.find(start_tag)
    end_index = contents.find(end_tag)
    return contents[(len("<title>") + start_index):end_index]


# helper function to get full url
# if url starts with ./
#   combine it with seed url
# else
#   use the url
def get_full_url(url, base):
    if url.startswith('./'):
        # add to the seed url
        start = url.find("./")
        end = base.rfind("/")
        full = base[:end] + url[start + 1:]
        return full
    else:
        return url


def get_dirname(full):
    start = full.rfind("/")
    end = full.rfind(".html")
    dirname = full[start + 1:end]
    file_path = os.path.join("data", dirname)
    return file_path


def create_directory(dirname):
    os.makedirs(dirname)


def create_file(dirname, filename):
    file_path = os.path.join(dirname, filename)
    fileout = open(file_path, "w")
    fileout.close()


def write_to_file(dirname, filename, content):
    file_path = os.path.join(dirname, filename)
    fileout = open(file_path, "w")
    fileout.write(json.dumps(content))
    fileout.close()


def delete_files():
    os.system("rm -rf data")


def setup_files(dir_name):
    create_directory(dir_name)
    create_file(dir_name, "title.txt")
    create_file(dir_name, "words.txt")
    create_file(dir_name, "incoming_links.txt")
    create_file(dir_name, "outgoing_links.txt")
    create_file(dir_name, "page_rank.txt")
    create_file(dir_name, "tf.txt")
    # create_file(dir_name, "idf.txt")
    create_file(dir_name, "tf-idfs.txt")
    create_file(dir_name, "vector.txt")


def computation_process(links_visited, unique_words):
    idf = {}
    for link in links_visited:
        dirname = get_dirname(link)
        page_rank = searchdata.get_page_rank(link)
        tf = {}
        tf_idf = {}
        vector = []
        for word in unique_words:
            tf[word] = searchdata.get_tf(link, word)
            idf[word] = searchdata.get_idf(word)
            tf_idf[word] = (searchdata.get_tf_idf(link, word))
            vector.append(searchdata.get_tf_idf(link, word))

        write_to_file(dirname, "page_rank.txt", page_rank)
        write_to_file(dirname, "tf.txt", tf)
        write_to_file(dirname, "tf-idfs.txt", tf_idf)
        write_to_file(dirname, "vector.txt", vector)

    write_to_file("data", "idf.txt", idf)


def crawl(seed):
    delete_files()

    incoming_links = {}
    unique_words = []

    queue = [seed]
    links_visited = {}
    ID = 0
    links_visited[seed] = ID

    # while queue is not empty
    while queue:
        # read the top URL
        contents = webdev.read_url(queue[0])

        # set up files
        dirname = get_dirname(queue[0])
        setup_files(dirname)

        # write title to title.txt
        write_to_file(dirname, "title.txt", get_title(contents))

        # call parse_words function and input contents as parameter
        # return a list of words in one page
        words = parse_words(contents)
        all_words = {}

        # add words in the all_words dictionary
        for w in words:

            if w not in unique_words:
                unique_words.append(w)

            if w not in all_words:
                all_words[w] = 1
            else:
                all_words[w] += 1

        # call parse_links function and input contents as parameter
        # return a list of links in one page
        links = parse_links(contents)

        # outgoing_links list
        outgoing_links = []

        # add links to the queue if not already looked at
        for l in links:
            full_link = get_full_url(l, seed)

            outgoing_links.append(full_link)

            if full_link in incoming_links:
                incoming_links[full_link].append(queue[0])
            else:
                incoming_links[full_link] = [queue[0]]

            if full_link not in links_visited:
                ID += 1
                links_visited[full_link] = ID
                queue.append(full_link)

        # BEFORE REMOVING, ADD CONTENTS TO FILES
        write_to_file(dirname, "outgoing_links.txt", outgoing_links)
        write_to_file(dirname, "words.txt", all_words)

        # remove the first URL
        queue.pop(0)

    for key in incoming_links:
        write_to_file(get_dirname(key), "incoming_links.txt",
                      incoming_links[key])

    write_to_file("data", "length.txt", len(links_visited))
    write_to_file("data", "links_visited.txt", links_visited)
    write_to_file("data", "unique_words.txt", unique_words)

    computation_process(links_visited, unique_words)

    return len(links_visited)


crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
