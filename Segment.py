class Segment:

    def __init__(self, xi, xf):
        self.xi = xi
        self.xf = xf
    
    def is_subset(self, segment_2):
        return self.xi >= segment_2.xi and self.xf <= segment_2.xf
    
    def intersects(self, segment_2):
        is_after = self.xi > segment_2.xi and self.xi > segment_2.xf
        is_before = self.xf < segment_2.xi and self.xf < segment_2.xf
        return not (is_after or is_before)
    
    def union(self, segment_2):
        if self.intersects(segment_2):
            xi = min([self.xi, segment_2.xi])
            xf = max([self.xf, segment_2.xf])
            return Segment(xi, xf), True
        else:
            return None, False        
    
    def __str__(self):
        return 'xi: ' + str(self.xi) + ' xf: ' + str(self.xf)

def group_all_segments(all_seg):
    final_seg = list(all_seg)
    while(True):
        group_result = group_one_segment(final_seg)
        if group_result == []:
            break
        final_seg = group_result
    return final_seg
    
def group_one_segment(all_seg):

    for i in range(len(all_seg) - 1):
        for j in range(i + 1, len(all_seg)):
            segi = all_seg[i]
            segj = all_seg[j]
            seg_res, status = segi.union(segj)
            if status:
                del all_seg[j]
                del all_seg[i]
                all_seg.append(seg_res)
                return all_seg    
    return []
    
def test():
    seg1 = Segment(1,5)
    seg2 = Segment(2,3)
    seg3 = Segment(-3,0)
    seg4 = Segment(0,4)
    seg5 = Segment(3,9)
    seg6 = Segment(5,12)
    seg7 = Segment(19,33)        
    answers = []
    answers.append(seg2.is_subset(seg1))
    answers.append(seg1.is_subset(seg2))
    answers.append(seg1.intersects(seg2))
    answers.append(seg1.intersects(seg3))
    answers.append(seg1.intersects(seg4))
    answers.append(seg1.intersects(seg5))
    answers.append(seg1.intersects(seg6))
    answers.append(seg1.intersects(seg7))
    assert(answers == [True, False, True, False, True, True, True, False])
    print('Segment test passed')
    
    all_seg = [seg1, seg2, seg3, seg4, seg5, seg6, seg7]
    final_seg = group_all_segments(all_seg)
    assert([final_seg[0].xi, final_seg[0].xf, final_seg[1].xi, final_seg[1].xf] == \
           [19, 33, -3, 12])
    