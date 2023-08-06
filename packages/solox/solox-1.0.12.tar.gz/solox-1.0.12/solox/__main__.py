from __future__ import absolute_import
import multiprocessing
import web



def main():
    try:
        pool = multiprocessing.Pool(processes=2)
        pool.apply_async(web.start_web)
        pool.apply_async(web.open_url)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print('stop solox success')


if __name__ == '__main__':
    main()

