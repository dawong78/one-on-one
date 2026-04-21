import { inject } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { catchError, filter, take, switchMap } from 'rxjs/operators';
import { Auth } from './auth';

var isRefreshing = false;
const refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

export const authInterceptor: HttpInterceptorFn = (req, next) => {

  const authService = inject(Auth);

  // Retrieve token from storage (e.g., localStorage or a service)
  const access_token = localStorage.getItem('access_token');
  
  // If token exists, clone request and set headers
  if (access_token) {
    const cloned = req.clone({
      setHeaders: {
        Authorization: `Bearer ${access_token}`
      }
    });
    // return next(cloned);
    return next(cloned).pipe(
      catchError(error => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          console.log("encountered jwt error");
          console.log(error);
          if (!isRefreshing) {
            isRefreshing = true;
            refreshTokenSubject.next(null);

            const refresh_token = localStorage.getItem('refresh_token') ?? '';
            return authService.refreshToken(refresh_token).pipe(
              switchMap((newToken) => {
                isRefreshing = false;
                refreshTokenSubject.next(newToken.access)
                localStorage.setItem('access_token', newToken.access);
                localStorage.setItem('refresh_token', newToken.refresh);
                const refreshedRequest = req.clone({
                  setHeaders: {
                    Authorization: `Bearer ${newToken.access}`
                  }
                });
                return next(refreshedRequest);
              }),
              catchError((err) => {
                isRefreshing = false;
                return throwError(() => err);
              })
            );
          }
          // Queue subsequent requests while refreshing
          return refreshTokenSubject.pipe(
            filter(token => token !== null),
            take(1),
            switchMap((token) => next(
              req.clone({
                setHeaders: {
                  Authorization: `Bearer ${token.access}`
                }
              })
            ))
          );
        }
        return throwError(() => error);
      })
    );
  }
  
  return next(req);
};

