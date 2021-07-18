def minDis(s1, s2, n, m, dp) :
            
    # If any string is empty,
    # return the remaining characters of other string		
    if(n == 0) :
        return m	
    if(m == 0) :
        return n
                        
    # To check if the recursive tree
    # for given n & m has already been executed
    if(dp[n][m] != -1) :
        return dp[n][m];
                    
    # If characters are equal, execute
    # recursive function for n-1, m-1
    if(s1[n - 1] == s2[m - 1]) :		
        if(dp[n - 1][m - 1] == -1) :
            dp[n][m] = minDis(s1, s2, n - 1, m - 1, dp)
            return dp[n][m]				
        else :
            dp[n][m] = dp[n - 1][m - 1]
            return dp[n][m]
            
    # If characters are nt equal, we need to		
    # find the minimum cost out of all 3 operations.		
    else :		
        if(dp[n - 1][m] != -1) :
            m1 = dp[n - 1][m]	
        else :
            m1 = minDis(s1, s2, n - 1, m, dp)
                
        if(dp[n][m - 1] != -1) :			
            m2 = dp[n][m - 1]		
        else :
            m2 = minDis(s1, s2, n, m - 1, dp)
        if(dp[n - 1][m - 1] != -1) :
            m3 = dp[n - 1][m - 1]
        else :
            m3 = minDis(s1, s2, n - 1, m - 1, dp)
        
        dp[n][m] = 1 + min(m1, min(m2, m3))
        return dp[n][m]
	
def main():
    salut=["mr.","mr","mrs.","mrs","ms.","ms","shri.","shri","smt.","smt"]
    str1 = input("").strip()
    str2 = input("").strip()
    str1=str1.lower()
    str2=str2.lower()
    lst=str2.split(" ")
    str2=""
    str2r=""
    if(lst[0] in salut):
        str2="".join(lst[1::])
        lstr=lst[1::1]
    else :
        str2="".join(lst)
        lstr=lst
    lstr=lstr[::-1]
    str2r="".join(lstr)
    lst1=str1.split()
    str1=""
    str1r=""
    if(lst1[0] in salut):
        str1="".join(lst1[1::])
        lst1r=lst1[1::1]
    else :
        str1="".join(lst1)
        lst1r=lst1
    lst1r=lst1r[::-1]
    str1r="".join(lst1r)
    n = len(str1)
    m = len(str2)
    res = list(filter(lambda x:  x in lst, lst1))
    if (1-(minDis(str1, str2r, n, m, dp = [[-1 for i in range(m + 1)] for j in range(n + 1)])/max(n,m)))>=0.8 :
        print("Match",end="")
    elif(1-(minDis(str1, str2, n, m, dp = [[-1 for i in range(m + 1)] for j in range(n + 1)])/max(n,m)))>=0.8:
        print("Match",end="")
    elif (1-(minDis(str1r, str2, n, m, dp = [[-1 for i in range(m + 1)] for j in range(n + 1)])/max(n,m)))>=0.8:
        print("Match",end="")
    elif len(res)==len(lstr) or len(res)==len(lst1r) :
        print("Match",end="")
    elif len(res)==1 and lstr[-1]==lst1r[-1][0] and lstr[-2]==lst1r[-2][0]:
        print("Match",end="")
    else:
        print("No Match",end="")
    #print(res,minDis(str1, str2, n, m, dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]))
main()	