import tqdm

from rectangle_expansion import is_inside, rect_in_list, add_to_rectangles, rectangles_expansion
from Cuboids import Cuboids


def jetta_expansion(cuboids):
    merge_sites = mergeable_yi(cuboids)
    final_space = Cuboids()
    for mergei in merge_sites:
        yi = min(mergei.get_all_yi())
        yf_rectangles = expand_cuboids(mergei)
        final_space = clean_downstairs_rectangles(final_space, yi, yf_rectangles)
    for cuboid in cuboids.all_not_mergeables().cuboids:
        final_space.add(cuboid.yi, cuboid.yf, cuboid.rect.copy())
    final_space.cuboids = eliminate_all_duplicates(final_space.cuboids)
    final_space.reset_id()
    return final_space

def add_reward_hacking(cuboids, max_cuboids_number):
    n_add = max_cuboids_number - len(cuboids) - 1
    cub_max, max_index = cuboids.cuboid_max_volume()
    del cuboids.cuboids[max_index]
    cub_left = cub_max.copy()
    cub_left.rect.segx.xf -= 1e-4
    cuboids.add(cub_left.yi, cub_left.yf, cub_left.rect.copy())
    cub_right = cub_max.copy()
    cub_right.rect.segx.xi += 1e-4
    cuboids.add(cub_right.yi, cub_right.yf, cub_right.rect.copy())    
    for i in range(n_add):
        cub_new = cub_left.copy()
        cub_new.rect.segx.xi += i * 1e-7
        cub_new.rect.segx.xf += i * 1e-7
        cuboids.add(cub_new.yi, cub_new.yf, cub_new.rect.copy())
    cuboids.reset_id()
    return cuboids

def check_r3_spaces(cuboids_input, cuboids_output):
    for cuboid in tqdm.tqdm(cuboids_input.cuboids):
        recti = cuboid.rect.copy()
        rect_list = cuboids_output.rectangles_with_ylimits(cuboid.yi, cuboid.yf)
        if not is_inside(recti, rect_list):
            print('Input was not described completely')
            return
    print('Input is inside output space')
    for cuboid in tqdm.tqdm(cuboids_output.cuboids):
        recti = cuboid.rect.copy()
        rect_list = cuboids_input.rectangles_with_ylimits(cuboid.yi, cuboid.yf)
        if not is_inside(recti, rect_list):
            print('Output exceeded R3 space')
            return
    print('Output is inside input space')

def mergeable_yi(cuboids):
    
    merge_sites = []
    yi_mergeables = cuboids.yi_mergeables()
    for yi in yi_mergeables:
        merge_sites.append(cuboids.all_withyi(yi))
    return merge_sites
 
def expand_cuboids(ystart_cuboids):
    all_rect = []
    saved_rectangles = {}
    yf_descending = sort_yf(ystart_cuboids)
    for referenceyf in yf_descending:
    
        new_rect_list = ystart_cuboids.rectangles_withyf(referenceyf, 'equal')
        for new_rect in new_rect_list:
            if not rect_in_list(new_rect, all_rect):
                all_rect = add_to_rectangles(new_rect, all_rect)
                all_rect = rectangles_expansion(all_rect)
    
        saved_rectangles[referenceyf] = all_rect
    
    return saved_rectangles
    
def sort_yf(mergeables):
    yf_l = mergeables.get_all_yf()
    yf_l.sort(reverse=True)
    return yf_l

def clean_downstairs_rectangles(final_space, yi, yf_rectangles):
    yf_l = list(yf_rectangles.keys())
    yf_l.sort(reverse=True)
    
    for rect in yf_rectangles[yf_l[0]]:
        final_space.add(yi, yf_l[0], rect)
    rect_previous_space = [rect.copy() for rect in yf_rectangles[yf_l[0]]]
    
    for i in range(1, len(yf_l)):
        rect_space = yf_rectangles[yf_l[i]]    
        j = 0 
        while(j < len(rect_space)):
            recti = rect_space[j]
            if rect_in_list(recti, rect_previous_space):
                del rect_space[j]
            else:
                j += 1    
    
        rect_previous_space += [rect.copy() for rect in rect_space]
        for rect in yf_rectangles[yf_l[i]]:
            final_space.add(yi, yf_l[i], rect)
    
    return final_space

def eliminate_all_duplicates(cuboid_list): # TODO - MERGE THIS FUNCTION WITH THE RECTANGLE ONE
    i = 0
    while(i < len(cuboid_list) - 1):
        j = i + 1
        while(j < len(cuboid_list)):
            cuboidi = cuboid_list[i]
            cuboidj = cuboid_list[j]
            if cuboidi.is_subset(cuboidj):
                del cuboid_list[i]
                i -= 1
                break
            elif cuboidj.is_subset(cuboidi):
                del cuboid_list[j]
            else:
                j += 1
        i += 1
    return cuboid_list

