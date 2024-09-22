import { useState, useEffect } from 'react';

function useIsTabActive() {
  const [isTabActive, setIsTabActive] = useState(true);
  const [count,setcount] = useState(0)

  useEffect(() => {
    const handleVisibilityChange = () => {
      setIsTabActive(!document.hidden);
      setcount(count+1)
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  return isTabActive;
}

export default useIsTabActive;
