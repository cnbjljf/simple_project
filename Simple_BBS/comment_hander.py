#
def add_node(tree_dic,comment):
    '''
    :param tree_dic:
    :param comment:
    :return:
    '''
    if comment.parent_comment is None:
        # i am  in top, so let me stay here
        tree_dic[comment] = {}
    else:
        # loop  this dict , until find
        for k,v in tree_dic.items():
            # find your father
            if k == comment.parent_comment:
                print('find your dad:',k)
                tree_dic[comment.parent_comment][comment] = {}
            else:
                # go to the next layer to  find
                print('keep going deeper ')
                add_node(v,comment)

def render_tree_node(tree_dic,margin_val):
    '''

    :param tree_dic:
    :param margin_val:
    :return:
    '''
    html = ''
    for k,v in tree_dic.items():
        ele = "<div class='comment-node' style='margin-left: %spx' >" % margin_val + k.comment +  \
            "<span style='margin-left:20px'>%s</span>" %(k.date.strftime("%Y/%m/%d %H:%I:%S")) \
            + "<span style='margin-left:20px'>%s</span>" %k.user.name + \
            "<input style='display: none' type='text' class='parent_id' name='parent_id' value='%s'> \
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <button onclick='expansion_comment(this)'\
          type='button'  class='btn btn-default'>" \
            %k.id  + "<span class='glyphicon glyphicon-edit' aria-hidden='true'></span>" + "</div>"
        html += ele
        html += render_tree_node(v,margin_val+16)
    return html


def render_comment_tree(tree_dic):
    '''

    :param tree_dic:
    :return:
    '''
    html = ''
    for k,v in tree_dic.items():
        ele = "<div class='root-comment'>" + k.comment + "<span style='margin-left:20px'>%s </span>" \
              %(k.date.strftime("%Y/%m/%d %H:%I:%S")) + "<span style='margin-left:20px'>%s</span>" %k.user.name + "\
            <input style='display: none' type='text' class='parent_id' name='parent_id' value='%s'> \
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <button onclick='expansion_comment(this)'\
            type='button'  class='btn btn-default'>" \
              %k.id  + "<span class='glyphicon glyphicon-edit' aria-hidden='true'></span>" + "</button></div>"
        html += ele
        html +=render_tree_node(v,10)
    return html


def build_tree(comment_tree):
    '''

    :param comment_tree:
    :return:
    '''
    tree_dic = {}
    for comment in comment_tree:
        add_node(tree_dic,comment)
    print('---------')
    for k,v in tree_dic.items():
        print(k,v)
    return tree_dic