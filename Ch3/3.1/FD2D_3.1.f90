!========================================================
!   Purpose: 2D TM
!
!   Methods: FDTD
!       
!       Date        Programer       Description of change
!       ====        =========       =====================
!      9/11/20       MorrisH        Original Code
!========================================================
PROGRAM main
    IMPLICIT NONE
    ! number of cells to be used
    INTEGER(8), PARAMETER :: IE = 60
    INTEGER(8), PARAMETER :: JE = 60
    REAL(8), PARAMETER :: pi = 3.14159265359
    REAL(8) :: ga(IE, JE), Dz(IE, JE), Ez(IE, JE)
    REAL(8) :: Hx(IE, JE), Hy(IE, JE)
    INTEGER(8) :: l, n, i, j, ic, jc, T
    REAL(8) :: ddx, dt, epsz, eps, sigma, eaf
    REAL(8) :: t0, width, pulse
    ! name of write file
    CHARACTER(len=15) :: str1
    CHARACTER(len=8) :: fmt
    fmt = '(I4.4)'

    ic = IE / 2
    jc = JE / 2
    ddx = 0.01
    dt = ddx / 6e8
    epsz = 8.8e-12

    Dz = 0.0
    Ez = 0.0
    Hx = 0.0
    Hy = 0.0
    ga = 1.0

    t0 = 20.0
    width = 6.0
    T = 0

    steploop: do T = 0, 1000
        !!! START FDTD !!!
        ! calculate Dx field
        do j = 2, JE
            do i = 2, IE 
                Dz(i, j) = Dz(i, j) + 0.5 * (Hy(i, j) - &
                           Hy(i-1, j) - Hx(i, j) + &
                           Hx(i, j-1))
            end do
        end do

        ! put gaussian pulse in the center
        pulse = exp(-0.5 * ((t0 - T) / width) ** 2.0)
        Dz(ic, jc) = pulse

        ! calculate Ez field
        do j = 2, JE
            do i = 2, IE
                Ez(i, j) = ga(i, j) * Dz(i, j)
            end do 
        end do

        ! calculate Hx field
        do j = 1, JE-1
            do i = 1, IE-1
                Hx(i, j) = Hx(i, j) + 0.5 * (Ez(i, j) - &
                           Ez(i, j+1))
           end do
       end do 

        ! calculate Hy field
        do j = 1, JE-1
            do i = 1, IE-1
                Hy(i, j) = Hy(i, j) + 0.5 * (Ez(i+1, j) - &
                           Ez(i, j))
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
