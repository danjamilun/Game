
class Game:
    forbidden_states = [
        ["c", "g", "w"],
        ["g", "w"],
        ["c", "g"]
    ]

    def __init__(self, left=["w", "c", "g"], right=[], boat_side=False, children=[]):
        self.left = left
        self.right = right
        self.boat_side = boat_side
        self.children = children 

    def __str__(self):
        return str(self.left) + str(self.right) + ("-->Left" if not self.boat_side else "-->Right")
    
def action_left(node,previous_states):
    for i in node.left:
        new_left = node.left[:]
        new_left.remove(i)
        new_right = node.right[:]
        new_right.append(i)
        if(not state_in_previous(previous_states,new_left,new_right,not node.boat_side)):
            return i
    return None
def action_right(node,previous_states):
    for i in node.right:
        new_left = node.left[:]
        new_left.append(i)
        new_right = node.right[:]
        new_right.remove(i)
        if(not state_in_previous(previous_states, new_left, new_right,not node.boat_side)):
            return i
    return None
def generate(node, previous_states, parent, children,previous_states_temp):
        
        if not node.boat_side:
                i=action_left(node,previous_states_temp)
                if(i != None):
                    new_left = node.left[:]
                    new_left.remove(i)
                    new_right = node.right[:]
                    new_right.append(i)
                    if sorted(new_left) not in node.forbidden_states and not state_in_previous(previous_states, new_left, new_right, not node.boat_side):
                        child=Game(left=new_left,right=new_right,boat_side=not node.boat_side,children=[])
                        children.append(child)
                        parent[child] = node 
                        previous_states_temp.append(child)
                        
                        return generate(node,previous_states, parent, children,previous_states_temp)
                    else:
                        child=Game(left=new_left,right=new_right,boat_side=not node.boat_side,children=[])
                        previous_states_temp.append(child)
                        return generate(node,previous_states,parent,children,previous_states_temp)

                if sorted(node.left) not in node.forbidden_states and not state_in_previous(previous_states, node.left[:], node.right[:], not node.boat_side):
                    child=Game(left=node.left[:],right=node.right[:],boat_side=not node.boat_side,children=[])
                    children.append(child)
                    parent[child] = node 
                node.children = children
                return

                
        else:
                
                i=action_right(node,previous_states_temp)
                if(i != None):
                    new_left = node.left[:]
                    new_left.append(i)
                    new_right = node.right[:]
                    new_right.remove(i)
                    if sorted(new_right) not in node.forbidden_states and not state_in_previous(previous_states, new_left, new_right, not node.boat_side):
                        child=Game(left=new_left,right=new_right,boat_side=not node.boat_side,children=[])
                        children.append(child)
                        parent[child] = node 
                        previous_states_temp.append(child)
                        return generate(node,previous_states,parent,children,previous_states_temp)
                    else:
                        child=Game(left=new_left,right=new_right,boat_side=not node.boat_side,children=[])
                        previous_states_temp.append(child)
                        return generate(node,previous_states,parent,children,previous_states_temp)

                if sorted(node.right) not in node.forbidden_states and not state_in_previous(previous_states, node.left[:], node.right[:], not node.boat_side):
                    child=Game(left=node.left[:],right=node.right[:],boat_side=not node.boat_side,children=[])
                    children.append(child)
                    parent[child] = node 
                node.children = children
                return

def find_solution(root_node,use_bfs=False):
        
        to_visit = [root_node]
        node = root_node
        step=0
        previous_states = []
        parent = {root_node: None}
        while to_visit:
            node = to_visit.pop()
            if not state_in_previous(previous_states, node.left, node.right, node.boat_side):
                previous_states.append(node)
            generate(node,previous_states, parent,[],[])
            if use_bfs:           
                to_visit = to_visit + node.children
            else:
                to_visit=node.children + to_visit
            if sorted(node.right) == ["c", "g", "w"]:
                solution = []
                while node is not None:
                    solution = [node] + solution
                    node = parent[node]
                    step +=1
                return solution
        return None
def bestFS(root_node,heuristic):
        to_visit = [root_node]
        node = root_node
        step=0
        previous_states = []
        parent = {root_node: None}
        while to_visit:
            node = to_visit.pop()
            if not state_in_previous(previous_states, node.left, node.right, node.boat_side):
                previous_states.append(node)
            generate(node,previous_states, parent,[],[])
                       
            to_visit = to_visit + node.children
            to_visit = sorted(to_visit, key=heuristic)
            
            if sorted(node.right) == ["c", "g", "w"]:
                solution = []
                while node is not None:
                    solution = [node] + solution
                    node = parent[node]
                    step +=1
                return solution
        return None
def heuristic_func(node):
        return len(node.right)
def state_in_previous(previous_states, left, right, boat_side):
        for i in previous_states:
            if(sorted(left) == sorted(i.left) and
            sorted(right) == sorted(i.right) and
            boat_side == i.boat_side):
                return True

if __name__ == "__main__":
    root = Game()
    solution = find_solution(root,use_bfs=False)
    print("DFS rjesenje = [", end='')
    for i in solution:
        print(i, '\b, ', end='')
    print("\b\b]") 

    solution = find_solution(root,use_bfs=True)
    print("BFS rjesenje = [", end='')
    for i in solution:
        print(i, '\b, ', end='')
    print("\b\b]")

    solution=bestFS(root, heuristic_func)
    print("BestFS rjesenje = [", end='')
    for i in solution:
        print(i, '\b, ', end='')
    print("\b\b]") 


    