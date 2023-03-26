#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>
#include "sha256/sha256.h"
#include <vector>


std::string user_password;


std::string hash_it(std::string password)
{
    SHA256 sha256;
    return sha256(password);
}

void find_user_data(std::string line)
{
    int start_index = line.find(getlogin());
    for(size_t i = start_index; i < start_index + 100; i++)
    {
        user_password.push_back(line[i]);
    }
}


void read_shadow_file()
{
    std::ifstream shadow;
    std::string read;
    char content;


    shadow.open("/etc/shadow");
    if(shadow.is_open())
    {
        while(shadow.good())
        {
            content = shadow.get();
            read.push_back(content);
        }
    }
    find_user_data(read);
}


std::string split(std::string password_from_shadow)
{
    return password_from_shadow.substr(14, 66);
}


bool compare(std::string test_word_hash, std::string shadow_pass)
{
    if(std::equal(test_word_hash.begin(), test_word_hash.end(), shadow_pass.begin(), shadow_pass.end()))
    {
        return true;
    }
    return false;
}


void test()
{
    std::vector<std::string> words;
    std::ifstream dict;
    std::string read;
    std::string aux;
    char content;

    read_shadow_file();
    std::string pw_hash = split(user_password);

    dict.open("pw.txt");
    if(dict.is_open())
    {
        while (dict.good())
        {
            content = dict.get();
            read.push_back(content);
        }

        for(size_t i = 0; i < read.length(); i++)
        {
            if(read[i] == '\n')
            {
                words.push_back(aux);
                aux.clear();
            }else{
                aux.push_back(read[i]);
            }
        }
        for(auto i: words)
        {
            if(compare(hash_it(i), pw_hash)){
                std::cout << i << std::endl;
            }
        }
    }


}


int main()
{
    std::ios_base::sync_with_stdio(false);
    test();
    return EXIT_SUCCESS;
}
