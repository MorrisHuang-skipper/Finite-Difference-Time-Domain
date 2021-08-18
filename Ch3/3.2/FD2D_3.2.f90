!========================================================
!   Purpose: 2D TM with PML
!
!   Methods: FDTD + PML
!       
!       Date        Programer       Description of change
!       ====        =========       =====================
!      9/14/20       MorrisH        Original Code
!========================================================
PROGRAM main
    IMPLICIT NONE
    ! number of cells to be used
    INTEGER(8), PARAMETER :: IE = 60
    INTEGER(8), PARAMETER :: JE = 60
    REAL(8), PARAMETER :: pi = 3.14159265359
    REAL(8) :: ga(IE, JE), Dz(IE, JE), Ez(IE, JE)
    REAL(8) :: Hx(IE, JE), Hy(IE, JE)
    INTEGER(8) :: l, n, i, j, ic, jc, T, npml
    REAL(8) :: ddx, dt, epsz, eps, sigma, eaf
    REAL(8) :: t0, width, pulse
    REAL(8) :: xn, xxn, xnum, xd, curl_e
    REAL(8) :: gi2(IE), gi3(IE)
    REAL(8) :: gj2(JE), gj3(JE)
    REAL(8) :: fi1(IE), fi2(IE), fi3(IE)
    REAL(8) :: fj1(JE), fj2(JE), fj3(JE)
    REAL(8) :: ihx(IE, JE), ihy(IE, JE)
    ! name of write file
    CHARACTER(len=15) :: str1
    CHARACTER(len=8) :: fmt
    fmt = '(I4.4)'

    ! ic = IE / 2
    ! jc = JE / 2
    ic = 20
    jc = 25
    ddx = 0.01
    dt = ddx / 6e8
    epsz = 8.8e-12

    Dz = 0.0
    Ez = 0.0
    Hx = 0.0
    Hy = 0.0
    ga = 1.0
    ihx = 0.0
    ihy = 0.0

    t0 = 20.0
    width = 6.0
    T = 0

    ! PML parameter
    gi2 = 1.0
    gi3 = 1.0
    fi1 = 0.0
    fi2 = 1.0
    fi3 = 1.0
    gj2 = 1.0
    gj3 = 1.0
    fj1 = 0.0
    fj2 = 1.0
    fj3 = 1.0
    npml = 8

    do i = 1, npml+1
        xnum = npml - i
        xd = npml
        xxn = xnum / xd
        xn = 0.33 * xxn ** 3.0
        gi2(i) = 1.0 / (1.0 + xn)
        gi2(IE-1-i) = 1.0 / (1.0 + xn)
        gi3(i) = (1.0 - xn) / (1.0 + xn)
        gi3(IE-1-i) = (1.0 - xn) / (1.0 + xn)
        
        xxn = (xnum - 0.5) / xd
        xn = 0.25 * xxn ** 3.0
        fi1(i) = xn
        fi1(IE-2-i) = xn
        fi2(i) = 1.0 / (1.0 + xn)
        fi2(IE-2-i) = 1.0 / (1.0 + xn)
        fi3(i) = (1.0 - xn) / (1.0 + xn)
        fi3(IE-2-i) = (1.0 -xn) / (1.0 + xn)
    end do

    do j = 1, npml+1
        xnum = npml - j
        xd = npml
        xxn = xnum / xd
        xn = 0.33 * xxn ** 3.0
        gj2(j) = 1.0 / (1.0 + xn)
        gj2(JE-1-j) = 1.0 / (1.0 + xn)
        gj3(j) = (1.0 - xn) / (1.0 + xn)
        gj3(JE-1-j) = (1.0 - xn) / (1.0 + xn)
        
        xxn = (xnum - 0.5) / xd
        xn = 0.25 * xxn ** 3.0
        fj1(j) = xn
        fj1(JE-2-j) = xn
        fj2(j) = 1.0 / (1.0 + xn)
        fj2(JE-2-j) = 1.0 / (1.0 + xn)
        fj3(j) = (1.0 - xn) / (1.0 + xn)
        fj3(JE-2-j) = (1.0 -xn) / (1.0 + xn)
    end do


    steploop: do T = 0, 500
        !!! START FDTD !!!
        ! calculate Dx field
        do j = 2, JE
            do i = 2, IE 
                Dz(i, j) = gi3(i) * gj3(j) * Dz(i, j) + &
                           gi2(i) * gj2(J) * 0.5 * &
                           (Hy(i, j) - Hy(i-1, j) - &
                           Hx(i, j) + Hx(i, j-1))
            end do
        end do

        ! Sunusoidal Source
        ! pulse = sin(2 * pi * 1500 * 1e6 * dt * T)
        ! Dz(ic, jc) = pulse
        ! Guassian Pulse
        pulse = exp(-0.5 * ((t0 - T) / width) ** 2.0)
        Dz(ic, jc) = pulse

        ! calculate Ez field
        do j = 2, JE
            do i = 2, IE
                Ez(i, j) = ga(i, j) * Dz(i, j)
            end do 
        end do

        ! set Ez edges to 0, as part of the PML
        do j = 1, JE-1
            Ez(1, j) = 0.0
            Ez(IE-1, j) = 0.0
        end do
        do i = 1, IE-1
            Ez(i, 1) = 0.0
            Ez(i, JE-1) = 0.0
        end do

        ! calculate Hx field
        do j = 1, JE-1
            do i = 1, IE
                curl_e = Ez(i, j) - Ez(i, j+1)
                ihx(i, j) = ihx(i, j) + fi1(i) * curl_e
                Hx(i, j) = fj3(j) * Hx(i, j) + fj2(j) * &
                           0.5 * (curl_e + ihx(i, j))
           end do
       end do 

        ! calculate Hy field
        do j = 1, JE
            do i = 1, IE-1
                curl_e = Ez(i+1, j) - Ez(i, j)
                ihy(i, j) = ihy(i, j) + fj1(j) * curl_e
                Hy(i, j) = fi3(i) * Hy(i, j) + fi2(i) * &
                           0.5 * (curl_e + ihy(i, j))
            end do
        end do 

        !!! END FDTD !!!
        ! output Ex, Hy
        write(str1, fmt) T
        open(1, file='field/Ez/'//trim(str1)//'.dat', &
             status='unknown')
        do j = 1, JE
            do i = 1, IE
                write(1, *) i, j, Ez(i, j)
            end do
        end do
        close(1)
    end do steploop
END PROGRAM main
