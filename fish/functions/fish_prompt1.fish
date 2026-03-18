function fish_prompt
    set_color green
    echo -n "darova "
    set_color normal
    echo -n "you are in: "(prompt_pwd)
    set_color yellow
    echo -n " --> "
    set_color blue
end
