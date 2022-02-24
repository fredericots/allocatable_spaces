from Segment import group_all_segments
from Rectangle import Rectangle

# no full expansions da pra economizar .25 se fizer o cruzado xz uma vez so.

def rectangles_expansion(rect_others):

    i = 0
    while(i < len(rect_others)):
        recti = rect_others[i].copy()
        del rect_others[i]
        next_rects = full_expansions(recti, rect_others)
        if len(next_rects) == 0:
            rect_others.insert(i, recti)
            i += 1
        else:
            for nr in next_rects:
                rect_others = rect_others[:i] + add_to_rectangles(nr, rect_others[i:])
    return rect_others

def eliminate_all_duplicates(rect_others):
    i = 0
    while(i < len(rect_others) - 1):
        j = i + 1
        while(j < len(rect_others)):
            recti = rect_others[i]
            rectj = rect_others[j]
            if recti.is_subset(rectj):
                del rect_others[i]
                i -= 1
                break
            elif rectj.is_subset(recti):
                del rect_others[j]
            else:
                j += 1
        i += 1
    return rect_others

def is_inside(rect, rect_others):
    xf_target = rect.segx.xf
    r_expand = Rectangle(rect.segx.xi, rect.segx.xi, rect.segz.xi, rect.segz.xf)
    was_expanded = True
    while(was_expanded):
        new_xf, was_expanded = directed_expansion(r_expand, rect_others, 'xf')
        if new_xf >= xf_target:
            return True
        r_expand.segx.xf = new_xf
    return False

def rect_in_list(rect, rect_others):
    for recti in rect_others:
        if rect.is_subset(recti):
            return True
    return False
    

def add_to_rectangles(nr, rect_others):
    if rect_in_list(nr, rect_others):
        return rect_others

    rect_others = [nr] + rect_others
    i = 1
    while(i < len(rect_others)):
        if rect_others[i].is_subset(rect_others[0]):
            del rect_others[i]
        else:
            i += 1
    return rect_others

def full_expansions(rect, rect_others):
    next_rects = []
    xi = rect.get('xi')
    xf = rect.get('xf')
    zi = rect.get('zi')
    zf = rect.get('zf')

    new_xi, xi_exp = directed_expansion(rect, rect_others, 'xi')
    new_xf, xf_exp = directed_expansion(rect, rect_others, 'xf')
    if xi_exp or xf_exp:
        next_rects.append(Rectangle(new_xi, new_xf, zi, zf))
        
    new_zi, zi_exp = directed_expansion(rect, rect_others, 'zi')
    new_zf, zf_exp = directed_expansion(rect, rect_others, 'zf')
    if zi_exp or zf_exp:
        next_rects.append(Rectangle(xi, xf, new_zi, new_zf))
        
    return next_rects

def directed_expansion(rect, rect_others, direction):
    others_intersected = rect.find_intersects(rect_others, direction)
    touched_segs = touched_segments(direction, others_intersected)
    
    if check_full_expansion(direction, touched_segs, rect):
        dir_values = [rect.get(direction) for rect in others_intersected]
        expanded_value = min_expand_value(dir_values, direction)
        return expanded_value, True
    else:
        return rect.get(direction), False

def min_expand_value(values, direction):
    if direction == 'xf' or direction == 'zf':
        return min(values)
    elif direction == 'xi' or direction == 'zi':
        return max(values)

def touched_segments(direction, others_intersected):
    seg_cont = seg_continuity(direction)
    t_segments = [rect.get(seg_cont) for rect in others_intersected]
    t_segments = group_all_segments(t_segments)
    return t_segments

def check_full_expansion(direction, touched_segs, rect):
    if len(touched_segs) == 1:
        seg_cont = seg_continuity(direction)
        rect_touched_wall = rect.get(seg_cont)
        return rect_touched_wall.is_subset(touched_segs[0])
    else:
        return False
        
def seg_continuity(direction):
    if direction == 'xi' or direction == 'xf':
        return 'segz'
    elif direction == 'zi' or direction == 'zf':
        return 'segx'    

